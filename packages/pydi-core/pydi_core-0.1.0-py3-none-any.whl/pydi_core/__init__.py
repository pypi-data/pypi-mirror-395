"""
PyDI - A simple dependency injection container for Python.

PyDI provides a lightweight dependency injection framework with support for
different service lifetimes (singleton, scoped, transient), automatic
dependency resolution, circular dependency detection, and lazy initialization
through factories.

Example::

    from pydi_core import PyDI

    class ServiceA:
        pass

    class ServiceB:
        def __init__(self, service_a: ServiceA):
            self.service_a = service_a

    pydi = PyDI()
    pydi.register_service(ServiceA, PyDI.LIFETIME_SINGLETON)
    pydi.register_service(ServiceB, PyDI.LIFETIME_TRANSIENT)
    pydi.finalize()

    service_b = pydi.get_service(ServiceB)
"""

import inspect
from typing import Dict, Generic, Type, Any, TypeVar, get_args, get_origin

__all__ = [
    'PyDI',
    'ServiceFactory',
    'CircularDependencyError',
    'AlreadyFinalizedError',
    'InvalidLifetimeError',
    'UnknownDependencyError',
]


class CircularDependencyError(Exception):
    """Circular dependency error.

    This error is raised when a circular dependency is detected.

    A circular dependency is a dependency chain that forms a loop."""
    pass


class AlreadyFinalizedError(Exception):
    """Already finalized error.

    This error is raised when trying to register a service after the manager
    has been finalized."""
    pass


class InvalidLifetimeError(Exception):
    """Invalid lifetime error.

    This error is raised when trying to register a service with an invalid
    lifetime."""
    pass


class UnknownDependencyError(Exception):
    """Unknown dependency error.

    This error is raised when a service or a dependency are not found in the
    manager."""
    pass


T = TypeVar('T')


class ServiceFactory(Generic[T]):
    """
    Service factory class.

    This class is used to create a service instance lazily and can be used as a
    dependency in other services.

    Example::

        class ServiceA:
            pass

        class ServiceB:
            def __init__(self, service_a_factory: ServiceFactory[ServiceA]):
                self.service_a_factory = service_a_factory
                self.service_a_1 = self.service_a_factory.create_instance()
                self.service_a_2 = self.service_a_factory.create_instance()
                self.service_a_3 = self.service_a_factory.create_instance()

    """

    def __init__(self, service: Type[T], pydi: 'PyDI'):
        self.service_type = service
        self.pydi = pydi

    def create_instance(self) -> T:
        """
        Create an instance of the service.

        Note that the service lifetime is respected according to what was set
        when registering the service.

        :return: Service instance.
        :rtype: T
        """
        return self.pydi.get_service(self.service_type)


class PyDI:
    """
    A simple dependency injection container.

    This class is used to register services and resolve their dependencies.

    It is possible to register services with different lifetimes:

    - Singleton: The service is created only once.
    - Scoped: The service is created once per dependency resolution scope.
    - Transient: The service is created every time it is requested.

    The manager supports lazy initialization of services and detects
    circular dependencies.

    Type hints are used to resolve dependencies. It's also possible to use the
    own service name as a dependency.

    Example::

        from pydi import PyDI

        class ServiceA:
            pass

        class ServiceB:
            def __init__(self, service_a: ServiceA):
                self.service_a = service_a

        class ServiceC:
            def __init__(self, service_a: ServiceA, service_b: ServiceB):
                self.service_a = service_a
                self.service_b = service_b

        pyDI = PyDI()
        pyDI.register_service(ServiceA, PyDI.LIFETIME_SINGLETON)
        pyDI.register_service(ServiceB, PyDI.LIFETIME_SCOPED)
        pyDI.register_service(ServiceC, PyDI.LIFETIME_TRANSIENT)
        pyDI.finalize()

        service_c = pyDI.get_service(ServiceC)
        # service_c is an instance of ServiceC with dependencies injected
    """

    LIFETIME_SINGLETON = 1
    """The service is created only once.
    The same instance is returned every time."""
    LIFETIME_SCOPED = 2
    """The service is created once per dependency resolution scope.
    Within a single get_service() call, the same instance is reused."""
    LIFETIME_TRANSIENT = 3
    """The service is created every time it is requested."""

    def __init__(self) -> None:
        self.services: Dict[Type, Dict[str, Any]] = {}
        self.finalized: bool = False

    def register_service(self, service: Type, lifetime: int) -> None:
        """
        Register a service with the manager.

        The service is registered with a lifetime, which can be one of:
        - Singleton: The service is created only once.
        - Scoped: The service is created once per dependency resolution scope.
        - Transient: The service is created every time it is requested.

        :param service: The service class.
        :type service: Type
        :param lifetime: The service lifetime.
        :type lifetime: int
        :raises AlreadyFinalizedError: If the manager is already finalized.
        :raises InvalidLifetimeError: If the given lifetime is invalid.
        :raises UnknownDependencyError: If a dependency annotation is not
        found.
        """
        if self.finalized:
            raise AlreadyFinalizedError()
        if not isinstance(lifetime, int):
            raise InvalidLifetimeError("Lifetime must be an integer")
        if lifetime not in [
                self.LIFETIME_SINGLETON,
                self.LIFETIME_SCOPED,
                self.LIFETIME_TRANSIENT
        ]:
            raise InvalidLifetimeError(f"Unknown lifetime {lifetime}")
        dependencies = []
        for param_name, param in inspect.signature(service.__init__)\
                .parameters.items():
            if param_name == 'self':
                continue
            elif param.annotation == inspect.Parameter.empty:
                raise UnknownDependencyError(
                    f"Unknown dependency for {service.__name__}: {param_name}")
            if get_origin(param.annotation) == ServiceFactory:
                dependency = get_args(param.annotation)[0]
                is_factory = True
            else:
                dependency = param.annotation
                is_factory = False
            dependencies.append((param_name, dependency, is_factory))
        self.services[service] = {
            'lifetime': lifetime,
            'dependencies': dependencies,
            'instance': None,
            'factory': None
        }

    def finalize(self):
        """
        Finalize the manager.

        This method checks for all dependencies connections and finalizes them.

        It checks for missing dependencies and circular dependencies errors.

        Note: This method is called automatically when a service is requested.
        Manual calling is not needed.

        After finalization, no more services can be registered.

        :raises CircularDependencyError: If a circular dependency is detected.
        :raises UnknownDependencyError: If a dependency is not found.
        """
        if self.finalized:
            return
        for service, service_data in self.services.items():
            for _, dependency, _ in service_data['dependencies']:
                if dependency not in self.services:
                    raise UnknownDependencyError(
                        f"Dependency {dependency} not found in service "
                        f"{service}")
        for service, service_data in self.services.items():
            dependencies = [
                dependency[1] for dependency in service_data['dependencies']
            ]
            new_dependency = len(dependencies) > 0
            while new_dependency:
                new_dependency = False
                for dependency in dependencies:
                    for _, subdepend, _ in self.services[dependency][
                            'dependencies']:
                        if subdepend not in dependencies:
                            dependencies.append(subdepend)
                            new_dependency = True
            if service in dependencies:
                raise CircularDependencyError(
                    f"Circular dependency detected in {service.__name__}")
        self.finalized = True

    def get_service(self, service: Type[T]) -> T:
        """
        Get an instance of a service.

        The service is instantiated according to its lifetime and its
        dependencies are injected.

        :param service: The service class.
        :type service: Type[T]
        :return: The service instance.
        :rtype: T
        :raises CircularDependencyError: If a circular dependency is detected.
        :raises UnknownDependencyError: If a dependency is not found.
        """

        if not self.finalized:
            self.finalize()
        instance = self.__nested_get_service(service)
        for service_data in self.services.values():
            if service_data['lifetime'] != self.LIFETIME_SINGLETON:
                service_data['instance'] = None
        return instance

    def __nested_get_service(self, service: Type[T]) -> T:
        """
        Recursive helper method to get a service instance.

        This method resolves the dependencies of a service and creates an
        instance of it if needed according to lifetimes.

        :param service: The service class.
        :type service: Type[T]
        :return: The service instance.
        :rtype: T
        :raises UnknownDependencyError: If a dependency is not found.
        """
        entry = self.services.get(service, None)
        if entry is None:
            raise UnknownDependencyError(
                f"Service {service.__name__} not found")
        if entry['instance'] is None:
            entry['instance'] = self.__instantiate_service(service)
        instance = entry['instance']
        if entry['lifetime'] == self.LIFETIME_TRANSIENT:
            entry['instance'] = None
        return instance

    def __get_factory(self, service: Type[T]) -> ServiceFactory[T]:
        """
        Get the factory of a service.

        :param service: The service class.
        :type service: Type[T]
        :return: The service factory.
        :rtype: ServiceFactory[T]
        :raises UnknownDependencyError: If the service is not found.
        """
        entry = self.services.get(service, None)
        if entry is None:
            raise UnknownDependencyError(
                f"Service {service.__name__} not found")
        if entry['factory'] is None:
            entry['factory'] = ServiceFactory(service, self)
        return entry['factory']

    def __instantiate_service(self, service: Type[T]) -> T:
        """
        Create an instance of a service.

        If the service has dependencies, they are recursively resolved.

        When this method is called, the service is guaranteed to be registered
        and circular dependencies are checked.

        :param service: The service class.
        :type service: Type[T]
        :return: The service instance.
        :rtype: T
        :raises UnknownDependencyError: If a dependency is not found.
        """
        service_entry = self.services.get(service, None)
        if service_entry is None:
            raise UnknownDependencyError(
                f"Service {service.__name__} not found")
        params = {}
        for param, dependency, is_factory in service_entry['dependencies']:
            if is_factory:
                params[param] = self.__get_factory(dependency)
            else:
                params[param] = self.__nested_get_service(dependency)
        return service(**params)
