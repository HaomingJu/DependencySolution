import os
import sys
import ConfigParser

def ReadProperty(file_path):
    ProSet = {}
    with open(file_path) as file_handle:
        lines = file_handle.readlines()
        for line in lines:
            line = line.strip()
            if line.__len__() and line[0] != '#':
                key_value = line.split(": ")
                ProSet[key_value[0]] = key_value[1]
    return ProSet

def WriteProfile(src_dic, dst_file):
    config = ConfigParser.ConfigParser()
    config.add_section("settings")
    config.add_section("options")
    config.set("settings", "os", src_dic["OS"])
    config.set("settings", "arch", src_dic["Arch"])
    config.set("settings", "compiler", src_dic["Compiler"])
    config.set("settings", "compiler.version", src_dic["CompilerVersion"])
    config.set("settings", "compiler.libcxx", "libstdc++")
    config.set("settings", "build_type", src_dic["BuildType"])

    if src_dic["LibType"] == "Shared" or src_dic["LibType"] == "shared":
        config.set("options", "*:shared", "True")
    else:
        config.set("options", "*:shared", "False")


    with open(dst_file, 'w') as profile:
        config.write(profile)



def WriteConanfile(src_dic, dst_file):
    with open(dst_file, 'w') as profile:
        profile.write("[requires]\n")
        for key in src_dic.keys():
            if "DepsOn" in key:
                profile.write(src_dic[key].split(":")[0])
                profile.write("\n")

        profile.write("\n\n[generators]\ncmake\n")



if __name__ == "__main__":
    proset = ReadProperty("../build.property")
    WriteProfile(proset, "./.profile")
    WriteConanfile(proset, "./.conanfile")
