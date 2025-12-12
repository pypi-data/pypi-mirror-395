from PyInstaller.utils.hooks import get_package_paths
import os.path

(_, root) = get_package_paths('aspose')

datas = [(os.path.join(root, 'assemblies', 'imaging'), os.path.join('aspose', 'assemblies', 'imaging'))]

hiddenimports = [ 'aspose', 'aspose.pyreflection', 'aspose.pyio', 'aspose.pygc', 'aspose.pycore' ]

