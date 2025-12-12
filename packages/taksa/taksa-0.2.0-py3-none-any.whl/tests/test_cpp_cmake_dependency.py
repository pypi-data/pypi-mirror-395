import unittest, os
from taksa import CppCMakeDependency
from taksa import BuildType
import pathlib as pl

class TestCaseTaksa(unittest.TestCase):
    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))
        
    def assertIsDirectory(self, path):
        if not pl.Path(path).resolve().is_dir():
            raise AssertionError("Directory does not exist: %s" % str(path))
        
    def assertIsDirectoryExist(self, path):
        if pl.Path(path).resolve().is_dir():
            raise AssertionError("Directory does not exist: %s" % str(path))
    
    @classmethod
    def tearDownClass(self):
        print("Tearing down after tests")

class TestCppCMakeDependcy(TestCaseTaksa):
    GIT_CPP_CMAKE_TEST_DEPENDENCY_URL = "https://github.com/eProgD/test_cpp_cmake_dependency.git"
    CPP_CMAKE_TEST_DEPENDENCY_NAME = "test_cpp_cmake_dependency"
    def test_remove_dependency(self):
        cpp_cmake_dependency = CppCMakeDependency(self.GIT_CPP_CMAKE_TEST_DEPENDENCY_URL)
        cpp_cmake_dependency.remove()
        cpp_cmake_dependency.download()
        cpp_cmake_dependency.remove()
        self.assertIsDirectoryExist(cpp_cmake_dependency.path)

    def test_download_dependency(self):
        cpp_cmake_dependency = CppCMakeDependency(self.GIT_CPP_CMAKE_TEST_DEPENDENCY_URL)
        cpp_cmake_dependency.remove()
        cpp_cmake_dependency.download()
        self.assertEqual(cpp_cmake_dependency.name, self.CPP_CMAKE_TEST_DEPENDENCY_NAME)
        self.assertIsDirectory(cpp_cmake_dependency.path)

    def test_configure_depndency(self):
        cpp_cmake_dependency = CppCMakeDependency(self.GIT_CPP_CMAKE_TEST_DEPENDENCY_URL)
        cpp_cmake_dependency.remove()
        cpp_cmake_dependency.download()
        try: 
            for build_type in BuildType:
                cpp_cmake_dependency.configure(build_type)
        except Exception as e:
            self.assertRaises(e)

    def test_build_depndency(self):
        cpp_cmake_dependency = CppCMakeDependency(self.GIT_CPP_CMAKE_TEST_DEPENDENCY_URL)
        cpp_cmake_dependency.remove()
        cpp_cmake_dependency.download()
        try: 
            for build_type in BuildType:
                cpp_cmake_dependency.configure(build_type)
                cpp_cmake_dependency.build(build_type)
        except Exception as e:
            self.assertRaises(e)

    def test_install_depndency(self):
        cpp_cmake_dependency = CppCMakeDependency(self.GIT_CPP_CMAKE_TEST_DEPENDENCY_URL)
        cpp_cmake_dependency.remove()
        cpp_cmake_dependency.download()
        try: 
            for build_type in BuildType:
                cpp_cmake_dependency.configure(build_type)
                cpp_cmake_dependency.build(build_type)
                cpp_cmake_dependency.install(build_type)
        except Exception as e:
            self.assertRaises(e)

        pass

if __name__ == "__main__":
    unittest.main()