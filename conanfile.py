from conans import ConanFile, CMake, tools
import platform

class MariadbcconnectorConan(ConanFile):
    name = "MariaDB++"
    version = "0.1"
    license = "BSL-1.0"
    author = "Mempler me@mempler.de"
    url = ""
    description = "https://github.com/mempler/conan-mariadbpp"
    topics = ("mariadb", "database", "sql")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = ("mysql-connector-c/6.1.11@bincrafters/stable")

    def source(self):
        self.run("git clone --recurse-submodules -j8 https://github.com/viaduck/mariadbpp.git")
        self.run("cd mariadbpp")

        # Adding needed header.
        tools.replace_in_file("mariadbpp/CMakeLists.txt", "project(mariadbclientpp)",
        '''project(mariadbclientpp)
        include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
        conan_basic_setup()''')
        
        # Fix for Windows
        tools.replace_in_file("mariadbpp/CMakeLists.txt", "target_link_libraries(mariadbclientpp ${MariaDBClient_LIBRARIES} pthread)", "target_link_libraries(mariadbclientpp ${MariaDBClient_LIBRARIES} ${CONAN_LIBS})")

        # Remove find_package, this will be handled by conan
        tools.replace_in_file("mariadbpp/CMakeLists.txt", "find_package(MariaDBClient REQUIRED)", "")
        

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="mariadbpp")
        cmake.build()

    def package(self):
        self.copy("**", dst="include", src="mariadbpp/include")
        self.copy("*mariadbclientpp.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mariadbclientpp"]

