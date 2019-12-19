from conans import ConanFile, tools


class GlogConan(ConanFile):
    name = "gflag"  # TODO: The package name
    version = "2.2.2"  # TODO: The package version
    settings = "os", "compiler", "build_type", "arch"
    description = "<Description of Glog here>"
    url = "None"
    license = "MIT"
    author = "Trunk"  # TODO: The author
    topics = None
    exports_sources = name + "/*"  # XXX: The upload path

    def package(self):
        self.copy("*", src=self.name)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
