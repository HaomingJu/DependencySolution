from conans import ConanFile, tools


class GlogConan(ConanFile):
    name = "gflag"  # TODO: The package name
    version = "2.2.2"  # TODO: The package version
    description = "<Description of Glog here>"
    author = "Trunk"  # TODO: The author

    license = "MIT"
    topics = None
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    exports_sources = name + "/*"  # XXX: The upload path

    def package(self):
        self.copy("*", src=self.name)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
