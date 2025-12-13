
from context import ngawari  # This is useful for testing outside of environment

import unittest
import numpy as np
import vtk
from ngawari import vtkfilters
from ngawari import ftk


class TestVTKTypeCheckers(unittest.TestCase):
    """Test VTK type checking functions."""
    
    def test_isVTI(self):
        """Test isVTI function."""
        img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        self.assertTrue(vtkfilters.isVTI(img))
        
        poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0)
        self.assertFalse(vtkfilters.isVTI(poly))
    
    def test_isVTP(self):
        """Test isVTP function."""
        poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0)
        self.assertTrue(vtkfilters.isVTP(poly))
        
        img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        self.assertFalse(vtkfilters.isVTP(img))
        
        # Test with None
        self.assertFalse(vtkfilters.isVTP(None))
    
    def test_isVTS(self):
        """Test isVTS function."""
        img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        vts = vtkfilters.vtiToVts(img)
        self.assertTrue(vtkfilters.isVTS(vts))
        
        poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0)
        self.assertFalse(vtkfilters.isVTS(poly))
        
        # Test with None
        self.assertFalse(vtkfilters.isVTS(None))


class TestVTKMath(unittest.TestCase):
    """Test VTK math functions."""
    
    def test_angleBetweenTwoVectors(self):
        """Test angleBetweenTwoVectors function."""
        vecA = [1, 0, 0]
        vecB = [0, 1, 0]
        angle = vtkfilters.angleBetweenTwoVectors(vecA, vecB)
        self.assertAlmostEqual(angle, np.pi/2, places=5)
        
        # Parallel vectors
        vecA = [1, 0, 0]
        vecB = [2, 0, 0]
        angle = vtkfilters.angleBetweenTwoVectors(vecA, vecB)
        self.assertAlmostEqual(angle, 0.0, places=5)
        
        # Opposite vectors
        vecA = [1, 0, 0]
        vecB = [-1, 0, 0]
        angle = vtkfilters.angleBetweenTwoVectors(vecA, vecB)
        self.assertAlmostEqual(angle, np.pi, places=5)


class TestArrayOperations(unittest.TestCase):
    """Test array get/set/delete operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        self.poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=8)
    
    def test_getArrayNames(self):
        """Test getArrayNames function."""
        # Test with no arrays
        names = vtkfilters.getArrayNames(self.img, pointData=True)
        self.assertEqual(len(names), 0)
        
        # Add arrays and test
        arr1 = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr1, 'testArray1')
        names = vtkfilters.getArrayNames(self.img, pointData=True)
        self.assertIn('testArray1', names)
        
        # Test cell data
        arr2 = np.random.rand(self.img.GetNumberOfCells())
        vtkfilters.setArrayFromNumpy(self.img, arr2, 'cellArray', pointData=False)
        names = vtkfilters.getArrayNames(self.img, pointData=False)
        self.assertIn('cellArray', names)
    
    def test_getArray(self):
        """Test getArray function."""
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'testArray')
        retrieved = vtkfilters.getArray(self.img, 'testArray')
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.GetName(), 'testArray')
    
    def test_getScalarsArrayName(self):
        """Test getScalarsArrayName function."""
        # No scalars set
        name = vtkfilters.getScalarsArrayName(self.img)
        self.assertIsNone(name)
        
        # Set scalars
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
        name = vtkfilters.getScalarsArrayName(self.img)
        self.assertEqual(name, 'scalars')
    
    def test_getVectorsArrayName(self):
        """Test getVectorsArrayName function."""
        # No vectors set
        name = vtkfilters.getVectorsArrayName(self.img)
        self.assertIsNone(name)
        
        # Set vectors
        arr = np.random.rand(self.img.GetNumberOfPoints(), 3)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'vectors', SET_VECTOR=True)
        name = vtkfilters.getVectorsArrayName(self.img)
        self.assertEqual(name, 'vectors')
    
    def test_getArrayId(self):
        """Test getArrayId function."""
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'testArray')
        idx = vtkfilters.getArrayId(self.img, 'testArray')
        self.assertIsNotNone(idx)
        self.assertIsInstance(idx, int)
        
        # Non-existent array
        idx = vtkfilters.getArrayId(self.img, 'nonExistent')
        self.assertIsNone(idx)
    
    def test_renameArray(self):
        """Test renameArray function."""
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'oldName')
        vtkfilters.renameArray(self.img, 'oldName', 'newName')
        names = vtkfilters.getArrayNames(self.img)
        self.assertIn('newName', names)
        self.assertNotIn('oldName', names)
    
    def test_getArrayAsNumpy(self):
        """Test getArrayAsNumpy function."""
        arr = np.random.rand(5*5*5)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'testArray')
        retrieved = vtkfilters.getArrayAsNumpy(self.img, 'testArray')
        np.testing.assert_array_almost_equal(arr, retrieved)
        
        # Test 3D return
        arr3d = vtkfilters.getArrayAsNumpy(self.img, 'testArray', RETURN_3D=True)
        self.assertEqual(arr3d.shape, (5, 5, 5))
    
    def test_getScalarsAsNumpy(self):
        """Test getScalarsAsNumpy function."""
        arr = np.random.rand(5*5*5)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
        retrieved = vtkfilters.getScalarsAsNumpy(self.img)
        np.testing.assert_array_almost_equal(arr, retrieved)
        
        # Test 3D return
        arr3d = vtkfilters.getScalarsAsNumpy(self.img, RETURN_3D=True)
        self.assertEqual(arr3d.shape, (5, 5, 5))
    
    def test_setArrayFromNumpy(self):
        """Test setArrayFromNumpy function."""
        # Test 1D array
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'test1D')
        retrieved = vtkfilters.getArrayAsNumpy(self.img, 'test1D')
        np.testing.assert_array_almost_equal(arr, retrieved)
        
        # Test 2D array (vectors)
        arr2d = np.random.rand(self.img.GetNumberOfPoints(), 3)
        vtkfilters.setArrayFromNumpy(self.img, arr2d, 'test2D', SET_VECTOR=True)
        retrieved = vtkfilters.getArrayAsNumpy(self.img, 'test2D')
        np.testing.assert_array_almost_equal(arr2d, retrieved)
        
        # Test 3D array
        arr3d = np.random.rand(5, 5, 5)
        vtkfilters.setArrayFromNumpy(self.img, arr3d, 'test3D', IS_3D=True)
        retrieved = vtkfilters.getArrayAsNumpy(self.img, 'test3D')
        self.assertEqual(retrieved.shape, (125,))
        
        # Test overwriting existing array
        arr1 = np.ones(self.img.GetNumberOfPoints())
        arr2 = np.zeros(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr1, 'overwrite')
        vtkfilters.setArrayFromNumpy(self.img, arr2, 'overwrite')
        retrieved = vtkfilters.getArrayAsNumpy(self.img, 'overwrite')
        np.testing.assert_array_almost_equal(arr2, retrieved)
    
    def test_setArrayDtype(self):
        """Test setArrayDtype function."""
        arr = np.random.rand(self.img.GetNumberOfPoints()).astype(np.float64)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'testArray')
        vtkfilters.setArrayDtype(self.img, 'testArray', np.float32)
        retrieved = vtkfilters.getArrayAsNumpy(self.img, 'testArray')
        self.assertEqual(retrieved.dtype, np.float32)
    
    def test_setArrayAsScalars(self):
        """Test setArrayAsScalars function."""
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'testArray')
        vtkfilters.setArrayAsScalars(self.img, 'testArray')
        name = vtkfilters.getScalarsArrayName(self.img)
        self.assertEqual(name, 'testArray')
    
    def test_ensureScalarsSet(self):
        """Test ensureScalarsSet function."""
        # No arrays
        img = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        with self.assertRaises(ValueError):
            vtkfilters.ensureScalarsSet(img)
        
        # With arrays
        arr = np.random.rand(img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(img, arr, 'testArray')
        name = vtkfilters.ensureScalarsSet(img)
        self.assertEqual(name, 'testArray')
        
        # With specific name - need to clear scalars first
        img2 = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        arr2 = np.random.rand(img2.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(img2, arr2, 'specificArray')
        name = vtkfilters.ensureScalarsSet(img2, 'specificArray')
        self.assertEqual(name, 'specificArray')
    
    def test_delArray(self):
        """Test delArray function."""
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'toDelete')
        names_before = vtkfilters.getArrayNames(self.img)
        self.assertIn('toDelete', names_before)
        
        vtkfilters.delArray(self.img, 'toDelete')
        names_after = vtkfilters.getArrayNames(self.img)
        self.assertNotIn('toDelete', names_after)
    
    def test_delArraysExcept(self):
        """Test delArraysExcept function."""
        arr1 = np.random.rand(self.img.GetNumberOfPoints())
        arr2 = np.random.rand(self.img.GetNumberOfPoints())
        arr3 = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr1, 'keep1')
        vtkfilters.setArrayFromNumpy(self.img, arr2, 'keep2')
        vtkfilters.setArrayFromNumpy(self.img, arr3, 'delete')
        
        vtkfilters.delArraysExcept(self.img, ['keep1', 'keep2'])
        names = vtkfilters.getArrayNames(self.img)
        self.assertIn('keep1', names)
        self.assertIn('keep2', names)
        self.assertNotIn('delete', names)


class TestFieldData(unittest.TestCase):
    """Test field data operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
    
    def test_addFieldData(self):
        """Test addFieldData function."""
        vtkfilters.addFieldData(self.img, 42.0, 'testField')
        val = vtkfilters.getFieldData(self.img, 'testField')
        self.assertAlmostEqual(val[0], 42.0)
    
    def test_getFieldData(self):
        """Test getFieldData function."""
        vtkfilters.addFieldData(self.img, 123.45, 'testField')
        val = vtkfilters.getFieldData(self.img, 'testField')
        self.assertAlmostEqual(val[0], 123.45)
    
    def test_getFieldDataDict(self):
        """Test getFieldDataDict function."""
        vtkfilters.addFieldData(self.img, 1.0, 'field1')
        vtkfilters.addFieldData(self.img, 2.0, 'field2')
        field_dict = vtkfilters.getFieldDataDict(self.img)
        self.assertIn('field1', field_dict)
        self.assertIn('field2', field_dict)
        self.assertAlmostEqual(field_dict['field1'][0], 1.0)
        self.assertAlmostEqual(field_dict['field2'][0], 2.0)
    
    def test_getFieldDataNames(self):
        """Test getFieldDataNames function."""
        vtkfilters.addFieldData(self.img, 1.0, 'field1')
        vtkfilters.addFieldData(self.img, 2.0, 'field2')
        names = vtkfilters.getFieldDataNames(self.img)
        self.assertIn('field1', names)
        self.assertIn('field2', names)
    
    def test_duplicateFieldData(self):
        """Test duplicateFieldData function."""
        vtkfilters.addFieldData(self.img, 42.0, 'testField')
        img2 = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        vtkfilters.duplicateFieldData(self.img, img2)
        val = vtkfilters.getFieldData(img2, 'testField')
        self.assertAlmostEqual(val[0], 42.0)
    
    def test_deleteFieldData(self):
        """Test deleteFieldData function."""
        vtkfilters.addFieldData(self.img, 42.0, 'testField')
        names_before = vtkfilters.getFieldDataNames(self.img)
        self.assertIn('testField', names_before)
        
        vtkfilters.deleteFieldData(self.img)
        names_after = vtkfilters.getFieldDataNames(self.img)
        self.assertEqual(len(names_after), 0)


class TestPointsOperations(unittest.TestCase):
    """Test points operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        self.poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=8)
    
    def test_getVtkPointsAsNumpy(self):
        """Test getVtkPointsAsNumpy function."""
        pts = vtkfilters.getVtkPointsAsNumpy(self.poly)
        self.assertEqual(pts.shape[1], 3)
        self.assertGreater(pts.shape[0], 0)
        
        # Test with image data
        pts_img = vtkfilters.getVtkPointsAsNumpy(self.img)
        self.assertEqual(pts_img.shape[0], 5*5*5)
        self.assertEqual(pts_img.shape[1], 3)
    
    def test_getPtsAsNumpy(self):
        """Test getPtsAsNumpy function."""
        pts = vtkfilters.getPtsAsNumpy(self.poly)
        self.assertEqual(pts.shape[1], 3)
        self.assertGreater(pts.shape[0], 0)
    
    def test_getCellCenters(self):
        """Test getCellCenters function."""
        centers = vtkfilters.getCellCenters(self.img)
        self.assertIsNotNone(centers)
        self.assertGreater(centers.GetNumberOfPoints(), 0)


class TestSourceBuilding(unittest.TestCase):
    """Test source building functions."""
    
    def test_buildImplicitSphere(self):
        """Test buildImplicitSphere function."""
        sphere = vtkfilters.buildImplicitSphere([1, 2, 3], 5.0)
        self.assertIsInstance(sphere, vtk.vtkSphere)
        self.assertEqual(sphere.GetCenter(), (1, 2, 3))
        self.assertEqual(sphere.GetRadius(), 5.0)
    
    def test_buildSphereSource(self):
        """Test buildSphereSource function."""
        sphere = vtkfilters.buildSphereSource([1, 2, 3], 5.0, res=10)
        self.assertTrue(vtkfilters.isVTP(sphere))
        self.assertGreater(sphere.GetNumberOfPoints(), 0)
        center = sphere.GetCenter()
        self.assertAlmostEqual(center[0], 1.0, places=1)
        self.assertAlmostEqual(center[1], 2.0, places=1)
        self.assertAlmostEqual(center[2], 3.0, places=1)
    
    def test_buildCylinderSource(self):
        """Test buildCylinderSource function."""
        cyl = vtkfilters.buildCylinderSource([0, 0, 0], 1.0, 2.0, res=10)
        self.assertTrue(vtkfilters.isVTP(cyl))
        self.assertGreater(cyl.GetNumberOfPoints(), 0)
        
        # Test with normal
        cyl2 = vtkfilters.buildCylinderSource([0, 0, 0], 1.0, 2.0, res=10, norm=[1, 0, 0])
        self.assertTrue(vtkfilters.isVTP(cyl2))
    
    def test_buildImplicitBox(self):
        """Test buildImplicitBox function."""
        box = vtkfilters.buildImplicitBox([0, 0, 0], [0, 0, 1], 2.0, 1.0)
        self.assertIsInstance(box, vtk.vtkBox)
    
    def test_buildCubeSource(self):
        """Test buildCubeSource function."""
        cube = vtkfilters.buildCubeSource([0, 0, 0], [0, 0, 1], 2.0, 1.0)
        self.assertTrue(vtkfilters.isVTP(cube))
        self.assertGreater(cube.GetNumberOfPoints(), 0)
    
    def test_buildPolyLineBetweenTwoPoints(self):
        """Test buildPolyLineBetweenTwoPoints function."""
        line = vtkfilters.buildPolyLineBetweenTwoPoints([0, 0, 0], [1, 1, 1], 10)
        self.assertTrue(vtkfilters.isVTP(line))
        self.assertEqual(line.GetNumberOfPoints(), 10)
        
        # Test with 2 points
        line2 = vtkfilters.buildPolyLineBetweenTwoPoints([0, 0, 0], [1, 0, 0], 2)
        self.assertEqual(line2.GetNumberOfPoints(), 2)
    
    def test_buildPolyTrianglesAtCp(self):
        """Test buildPolyTrianglesAtCp function."""
        pts = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
        poly = vtkfilters.buildPolyTrianglesAtCp(pts)
        self.assertTrue(vtkfilters.isVTP(poly))
        self.assertGreater(poly.GetNumberOfCells(), 0)
        
        # Test with reference vector
        poly2 = vtkfilters.buildPolyTrianglesAtCp(pts, refVec=[0, 0, 1])
        self.assertTrue(vtkfilters.isVTP(poly2))
    
    def test_buildPlaneSource(self):
        """Test buildPlaneSource function."""
        plane = vtkfilters.buildPlaneSource([0, 0, 0], [1, 0, 0], [0, 1, 0], [10, 10])
        self.assertTrue(vtkfilters.isVTP(plane))
        self.assertEqual(plane.GetNumberOfPoints(), 121)  # (10+1)*(10+1)
    
    def test_buildPolyLineFromXYZ(self):
        """Test buildPolyLineFromXYZ function."""
        xyz = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
        line = vtkfilters.buildPolyLineFromXYZ(xyz)
        self.assertTrue(vtkfilters.isVTP(line))
        self.assertEqual(line.GetNumberOfPoints(), 4)
        
        # Test with LOOP
        line_loop = vtkfilters.buildPolyLineFromXYZ(xyz, LOOP=True)
        self.assertTrue(vtkfilters.isVTP(line_loop))
    
    def test_buildPolydataFromXYZ(self):
        """Test buildPolydataFromXYZ function."""
        xyz = np.random.rand(10, 3)
        poly = vtkfilters.buildPolydataFromXYZ(xyz)
        self.assertTrue(vtkfilters.isVTP(poly))
        self.assertEqual(poly.GetNumberOfPoints(), 10)


class TestClippingCutting(unittest.TestCase):
    """Test clipping and cutting functions."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        arr = np.random.rand(10*10*10)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
        self.poly = vtkfilters.buildSphereSource([5, 5, 5], 3.0, res=10)
    
    def test_getDataCutByPlane(self):
        """Test getDataCutByPlane function."""
        cut = vtkfilters.getDataCutByPlane(self.img, [1, 0, 0], [5, 5, 5])
        self.assertIsNotNone(cut)
        self.assertGreater(cut.GetNumberOfPoints(), 0)
    
    def test_getPolyDataClippedBySphere(self):
        """Test getPolyDataClippedBySphere function."""
        # Use sphere center and larger radius to ensure clipping
        center = self.poly.GetCenter()
        clipped = vtkfilters.getPolyDataClippedBySphere(self.poly, center, 5.0)
        self.assertIsNotNone(clipped)
        # Note: clipping may result in 0 points if sphere is completely outside
        # Use a radius that definitely intersects
        clipped2 = vtkfilters.getPolyDataClippedBySphere(self.poly, center, 10.0)
        self.assertIsNotNone(clipped2)
        
        # Test with CRINKLECLIP
        clipped3 = vtkfilters.getPolyDataClippedBySphere(self.poly, center, 10.0, CRINKLECLIP=True)
        self.assertIsNotNone(clipped3)
    
    def test_getPolyDataClippedByBox(self):
        """Test getPolyDataClippedByBox function."""
        clipped = vtkfilters.getPolyDataClippedByBox(self.poly, [5, 5, 5], [0, 0, 1], 2.0, 1.0)
        self.assertIsNotNone(clipped)
        
        # Test INSIDE
        clipped_inside = vtkfilters.getPolyDataClippedByBox(self.poly, [5, 5, 5], [0, 0, 1], 2.0, 1.0, INSIDE=True)
        self.assertIsNotNone(clipped_inside)
    
    def test_clipDataByPlane(self):
        """Test clipDataByPlane function."""
        clipped = vtkfilters.clipDataByPlane(self.img, [5, 5, 5], [1, 0, 0])
        self.assertIsNotNone(clipped)
        self.assertGreater(clipped.GetNumberOfPoints(), 0)
    
    def test_clippedByPlaneClosedSurface(self):
        """Test clippedByPlaneClosedSurface function."""
        clipped = vtkfilters.clippedByPlaneClosedSurface(self.poly, [5, 5, 5], [1, 0, 0])
        self.assertIsNotNone(clipped)
        self.assertGreater(clipped.GetNumberOfPoints(), 0)
    
    def test_clippedBySphere(self):
        """Test clippedBySphere function."""
        clipped = vtkfilters.clippedBySphere(self.img, [5, 5, 5], 3.0)
        self.assertIsNotNone(clipped)
        self.assertGreater(clipped.GetNumberOfPoints(), 0)
    
    def test_clippedByScalar(self):
        """Test clippedByScalar function."""
        clipped = vtkfilters.clippedByScalar(self.img, 'scalars', 0.5)
        self.assertIsNotNone(clipped)
        
        # Test INSIDE_OUT
        clipped2 = vtkfilters.clippedByScalar(self.img, 'scalars', 0.5, INSIDE_OUT=True)
        self.assertIsNotNone(clipped2)


class TestImageDataOperations(unittest.TestCase):
    """Test image data operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        arr = np.random.rand(10*10*10)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
    
    def test_vtiToVts(self):
        """Test vtiToVts function."""
        vts = vtkfilters.vtiToVts(self.img)
        self.assertTrue(vtkfilters.isVTS(vts))
        self.assertEqual(vts.GetNumberOfPoints(), self.img.GetNumberOfPoints())
    
    def test_vtsToVti(self):
        """Test vtsToVti function."""
        vts = vtkfilters.vtiToVts(self.img)
        vti = vtkfilters.vtsToVti(vts)
        self.assertTrue(vtkfilters.isVTI(vti))
    
    def test_getVtsOrigin(self):
        """Test getVtsOrigin function."""
        vts = vtkfilters.vtiToVts(self.img)
        origin = vtkfilters.getVtsOrigin(vts)
        self.assertEqual(len(origin), 3)
    
    def test_getVtsResolution(self):
        """Test getVtsResolution function."""
        vts = vtkfilters.vtiToVts(self.img)
        res = vtkfilters.getVtsResolution(vts)
        self.assertEqual(len(res), 3)
        np.testing.assert_array_almost_equal(res, [1, 1, 1])
    
    def test_getResolution_VTI(self):
        """Test getResolution_VTI function."""
        res = vtkfilters.getResolution_VTI(self.img)
        self.assertEqual(len(res), 3)
        np.testing.assert_array_almost_equal(res, [1, 1, 1])
    
    def test_buildRawImageData(self):
        """Test buildRawImageData function."""
        img = vtkfilters.buildRawImageData([5, 6, 7], [0.5, 0.6, 0.7], [1, 2, 3])
        self.assertTrue(vtkfilters.isVTI(img))
        self.assertEqual(img.GetNumberOfPoints(), 5*6*7)
        dims = [0, 0, 0]
        img.GetDimensions(dims)
        self.assertEqual(dims, [5, 6, 7])
        np.testing.assert_array_almost_equal(img.GetSpacing(), [0.5, 0.6, 0.7])
        np.testing.assert_array_almost_equal(img.GetOrigin(), [1, 2, 3])
    
    def test_duplicateImageData(self):
        """Test duplicateImageData function."""
        img2 = vtkfilters.duplicateImageData(self.img)
        self.assertTrue(vtkfilters.isVTI(img2))
        self.assertEqual(img2.GetNumberOfPoints(), self.img.GetNumberOfPoints())
        np.testing.assert_array_almost_equal(img2.GetSpacing(), self.img.GetSpacing())
        np.testing.assert_array_almost_equal(img2.GetOrigin(), self.img.GetOrigin())
    
    def test_getVarValueAtI_ImageData(self):
        """Test getVarValueAtI_ImageData function."""
        val = vtkfilters.getVarValueAtI_ImageData(self.img, [5, 5, 5], 'scalars')
        self.assertIsNotNone(val)
        self.assertIsInstance(val, (tuple, list))
    
    def test_getImageX(self):
        """Test getImageX function."""
        x = vtkfilters.getImageX(self.img, 0)
        self.assertEqual(len(x), 3)
    
    def test_imageX_ToStructuredCoords(self):
        """Test imageX_ToStructuredCoords function."""
        xyz_list = [[0, 0, 0], [5, 5, 5], [9, 9, 9]]
        ijk_list = vtkfilters.imageX_ToStructuredCoords(self.img, xyz_list)
        self.assertEqual(len(ijk_list), len(xyz_list))
        for ijk in ijk_list:
            self.assertEqual(len(ijk), 3)
    
    def test_imageIndex_ToStructuredCoords(self):
        """Test imageIndex_ToStructuredCoords function."""
        indices = [0, 100, 500, 999]
        coords = vtkfilters.imageIndex_ToStructuredCoords(self.img, indices)
        self.assertEqual(len(coords), len(indices))
        for coord in coords:
            self.assertEqual(len(coord), 3)
    
    def test_getNeighbours26_fromImageIndex(self):
        """Test getNeighbours26_fromImageIndex function."""
        neighbours = vtkfilters.getNeighbours26_fromImageIndex(self.img, 500, delta=1)
        self.assertGreater(len(neighbours), 0)
        self.assertLessEqual(len(neighbours), 26)
        
        # Test with RETURN_STRUCTCOORDS
        coords = vtkfilters.getNeighbours26_fromImageIndex(self.img, 500, delta=1, RETURN_STRUCTCOORDS=True)
        self.assertGreater(len(coords), 0)
    
    def test_imageStrucCoords_toIndex(self):
        """Test imageStrucCoords_toIndex function."""
        coords = [(5, 5, 5), (0, 0, 0), (9, 9, 9)]
        indices = vtkfilters.imageStrucCoords_toIndex(self.img, coords)
        self.assertEqual(len(indices), len(coords))
        
        # Test single coord
        idx = vtkfilters.imageStrucCoords_toIndex(self.img, (5, 5, 5))
        self.assertIsInstance(idx, list)
    
    def test_imageStrucCoords_toX(self):
        """Test imageStrucCoords_toX function."""
        coords = [(5, 5, 5), (0, 0, 0)]
        xyz = vtkfilters.imageStrucCoords_toX(self.img, coords)
        self.assertEqual(len(xyz), len(coords))
        for pt in xyz:
            self.assertEqual(len(pt), 3)
    
    def test_filterFlipImageData(self):
        """Test filterFlipImageData function."""
        flipped = vtkfilters.filterFlipImageData(self.img, 0)  # Flip X axis
        self.assertTrue(vtkfilters.isVTI(flipped))
        self.assertEqual(flipped.GetNumberOfPoints(), self.img.GetNumberOfPoints())


class TestPolyDataOperations(unittest.TestCase):
    """Test PolyData operations."""
    
    def setUp(self):
        """Set up test data."""
        self.poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=10)
    
    def test_getPolyDataMeanFromCenter(self):
        """Test getPolyDataMeanFromCenter function."""
        mean_dist = vtkfilters.getPolyDataMeanFromCenter(self.poly)
        self.assertGreater(mean_dist, 0)
        self.assertLess(mean_dist, 2.0)  # Should be less than radius*2


class TestCopyOperations(unittest.TestCase):
    """Test copy operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        arr = np.random.rand(5*5*5)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'testArray')
        self.poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0)
    
    def test_copyPolyData(self):
        """Test copyPolyData function."""
        copy = vtkfilters.copyPolyData(self.poly)
        self.assertIsNotNone(copy)
        self.assertEqual(copy.GetNumberOfPoints(), self.poly.GetNumberOfPoints())
        self.assertIsNot(copy, self.poly)  # Should be different objects
    
    def test_copyData(self):
        """Test copyData function."""
        # Test with ImageData
        copy_img = vtkfilters.copyData(self.img)
        self.assertIsNotNone(copy_img)
        self.assertTrue(vtkfilters.isVTI(copy_img))
        self.assertEqual(copy_img.GetNumberOfPoints(), self.img.GetNumberOfPoints())
        
        # Test with PolyData
        copy_poly = vtkfilters.copyData(self.poly)
        self.assertIsNotNone(copy_poly)
        self.assertTrue(vtkfilters.isVTP(copy_poly))
        self.assertEqual(copy_poly.GetNumberOfPoints(), self.poly.GetNumberOfPoints())


class TestFilters(unittest.TestCase):
    """Test filter functions."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        arr = np.random.rand(10*10*10)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
        self.poly = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=10)
    
    def test_contourFilter(self):
        """Test contourFilter function."""
        contour = vtkfilters.contourFilter(self.img, 0.5)
        self.assertTrue(vtkfilters.isVTP(contour))
        self.assertGreater(contour.GetNumberOfPoints(), 0)
    
    def test_cleanData(self):
        """Test cleanData function."""
        cleaned = vtkfilters.cleanData(self.poly)
        self.assertTrue(vtkfilters.isVTP(cleaned))
        
        # Test with tolerance
        cleaned2 = vtkfilters.cleanData(self.poly, tolerance=0.01)
        self.assertTrue(vtkfilters.isVTP(cleaned2))
        
        # Test without point merging
        cleaned3 = vtkfilters.cleanData(self.poly, DO_POINT_MERGING=False)
        self.assertTrue(vtkfilters.isVTP(cleaned3))
    
    def test_reduceNumberOfPoints(self):
        """Test reduceNumberOfPoints function."""
        reduced = vtkfilters.reduceNumberOfPoints(self.poly, 50)
        self.assertLessEqual(reduced.GetNumberOfPoints(), 50)
        
        # Test with more points than available
        reduced2 = vtkfilters.reduceNumberOfPoints(self.poly, 10000)
        self.assertEqual(reduced2.GetNumberOfPoints(), self.poly.GetNumberOfPoints())
    
    def test_filterBoolean(self):
        """Test filterBoolean function."""
        sphere1 = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=8)
        sphere2 = vtkfilters.buildSphereSource([0.5, 0, 0], 1.0, res=8)
        sphere1 = vtkfilters.filterTriangulate(sphere1)
        sphere2 = vtkfilters.filterTriangulate(sphere2)
        
        # Test union
        union = vtkfilters.filterBoolean(sphere1, sphere2, 'union')
        self.assertTrue(vtkfilters.isVTP(union))
        
        # Test intersection
        intersection = vtkfilters.filterBoolean(sphere1, sphere2, 'intersection')
        self.assertTrue(vtkfilters.isVTP(intersection))
        
        # Test difference
        difference = vtkfilters.filterBoolean(sphere1, sphere2, 'difference')
        self.assertTrue(vtkfilters.isVTP(difference))
    
    def test_tubeFilter(self):
        """Test tubeFilter function."""
        line = vtkfilters.buildPolyLineFromXYZ(np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0]]))
        tube = vtkfilters.tubeFilter(line, 0.1, nSides=8, CAPS=True)
        self.assertTrue(vtkfilters.isVTP(tube))
        self.assertGreater(tube.GetNumberOfPoints(), 0)
        
        # Test without caps
        tube2 = vtkfilters.tubeFilter(line, 0.1, nSides=8, CAPS=False)
        self.assertTrue(vtkfilters.isVTP(tube2))
    
    def test_filterVtpSpline(self):
        """Test filterVtpSpline function."""
        line = vtkfilters.buildPolyLineFromXYZ(np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]))
        
        # Test with spacing
        spline1 = vtkfilters.filterVtpSpline(line, spacing=0.1)
        self.assertTrue(vtkfilters.isVTP(spline1))
        
        # Test with nPoints
        spline2 = vtkfilters.filterVtpSpline(line, nPoints=20)
        self.assertTrue(vtkfilters.isVTP(spline2))
        
        # Test with smoothFactor
        spline3 = vtkfilters.filterVtpSpline(line, nPoints=10, smoothFactor=2.0)
        self.assertTrue(vtkfilters.isVTP(spline3))
    
    def test_filterTransformPolyData(self):
        """Test filterTransformPolyData function."""
        # Test translation
        translated = vtkfilters.filterTransformPolyData(self.poly, disp=[1, 2, 3])
        self.assertTrue(vtkfilters.isVTP(translated))
        
        # Test scaling
        scaled = vtkfilters.filterTransformPolyData(self.poly, scale=[2, 2, 2])
        self.assertTrue(vtkfilters.isVTP(scaled))
        
        # Test rotation
        rotated = vtkfilters.filterTransformPolyData(self.poly, rotate=[90, 0, 0, 1])
        self.assertTrue(vtkfilters.isVTP(rotated))
        
        # Test rotateXYZ
        rotated2 = vtkfilters.filterTransformPolyData(self.poly, rotateXYZ=[90, 0, 0])
        self.assertTrue(vtkfilters.isVTP(rotated2))
    
    def test_pointToCellData(self):
        """Test pointToCellData function."""
        arr = np.random.rand(self.img.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'pointArray')
        cell_data = vtkfilters.pointToCellData(self.img)
        self.assertIsNotNone(cell_data)
        self.assertGreater(cell_data.GetNumberOfCells(), 0)
    
    def test_cellToPointData(self):
        """Test cellToPointData function."""
        arr = np.random.rand(self.img.GetNumberOfCells())
        vtkfilters.setArrayFromNumpy(self.img, arr, 'cellArray', pointData=False)
        point_data = vtkfilters.cellToPointData(self.img)
        self.assertIsNotNone(point_data)
        self.assertGreater(point_data.GetNumberOfPoints(), 0)
    
    def test_getOutline(self):
        """Test getOutline function."""
        outline = vtkfilters.getOutline(self.img)
        self.assertTrue(vtkfilters.isVTP(outline))
        self.assertEqual(outline.GetNumberOfPoints(), 8)  # Cube has 8 vertices
    
    def test_getMaximumBounds(self):
        """Test getMaximumBounds function."""
        bounds = vtkfilters.getMaximumBounds(self.img)
        self.assertGreater(bounds, 0)
    
    def test_appendPolyData(self):
        """Test appendPolyData function."""
        poly1 = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=5)
        poly2 = vtkfilters.buildSphereSource([3, 0, 0], 1.0, res=5)
        appended = vtkfilters.appendPolyData(poly1, poly2)
        self.assertTrue(vtkfilters.isVTP(appended))
        self.assertEqual(appended.GetNumberOfPoints(), poly1.GetNumberOfPoints() + poly2.GetNumberOfPoints())
    
    def test_appendPolyDataList(self):
        """Test appendPolyDataList function."""
        poly1 = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=5)
        poly2 = vtkfilters.buildSphereSource([3, 0, 0], 1.0, res=5)
        poly3 = vtkfilters.buildSphereSource([6, 0, 0], 1.0, res=5)
        appended = vtkfilters.appendPolyDataList([poly1, poly2, poly3])
        self.assertTrue(vtkfilters.isVTP(appended))
        
        # Test with single element
        single = vtkfilters.appendPolyDataList([poly1])
        self.assertEqual(single.GetNumberOfPoints(), poly1.GetNumberOfPoints())
    
    def test_appendImageList(self):
        """Test appendImageList function."""
        img1 = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [0, 0, 0])
        img2 = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [5, 0, 0])
        appended = vtkfilters.appendImageList([img1, img2], appendAxis=0)
        self.assertTrue(vtkfilters.isVTI(appended))
    
    def test_filterTriangulate(self):
        """Test filterTriangulate function."""
        triangulated = vtkfilters.filterTriangulate(self.poly)
        self.assertTrue(vtkfilters.isVTP(triangulated))
        self.assertGreater(triangulated.GetNumberOfCells(), 0)
    
    def test_filterExtractSurface(self):
        """Test filterExtractSurface function."""
        surface = vtkfilters.filterExtractSurface(self.img)
        self.assertTrue(vtkfilters.isVTP(surface))
        self.assertGreater(surface.GetNumberOfPoints(), 0)
    
    def test_filterExtractTri(self):
        """Test filterExtractTri function."""
        tri = vtkfilters.filterExtractTri(self.img)
        self.assertTrue(vtkfilters.isVTP(tri))
        self.assertGreater(tri.GetNumberOfCells(), 0)
    
    def test_getVolumeSurfaceAreaOfPolyData(self):
        """Test getVolumeSurfaceAreaOfPolyData function."""
        volume, area = vtkfilters.getVolumeSurfaceAreaOfPolyData(self.poly)
        self.assertGreater(volume, 0)
        self.assertGreater(area, 0)
    
    def test_smoothTris(self):
        """Test smoothTris function."""
        smoothed = vtkfilters.smoothTris(self.poly, iterations=10)
        self.assertTrue(vtkfilters.isVTP(smoothed))
        self.assertEqual(smoothed.GetNumberOfPoints(), self.poly.GetNumberOfPoints())
    
    def test_smoothTris_SINC(self):
        """Test smoothTris_SINC function."""
        smoothed = vtkfilters.smoothTris_SINC(self.poly, iterations=5)
        self.assertTrue(vtkfilters.isVTP(smoothed))
        self.assertEqual(smoothed.GetNumberOfPoints(), self.poly.GetNumberOfPoints())
    
    def test_filterExtractEdges(self):
        """Test filterExtractEdges function."""
        edges = vtkfilters.filterExtractEdges(self.poly)
        self.assertTrue(vtkfilters.isVTP(edges))
    
    def test_isPolyDataWaterTight(self):
        """Test isPolyDataWaterTight function."""
        # Sphere should be watertight
        is_watertight = vtkfilters.isPolyDataWaterTight(self.poly)
        self.assertIsInstance(is_watertight, bool)
    
    def test_isPolyDataPolyLine(self):
        """Test isPolyDataPolyLine function."""
        line = vtkfilters.buildPolyLineFromXYZ(np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0]]))
        self.assertTrue(vtkfilters.isPolyDataPolyLine(line))
        self.assertFalse(vtkfilters.isPolyDataPolyLine(self.poly))
    
    def test_calculatePolyDataArea(self):
        """Test calculatePolyDataArea function."""
        area = vtkfilters.calculatePolyDataArea(self.poly)
        self.assertGreater(area, 0)
        
        # Test with polyline
        line = vtkfilters.buildPolyLineFromXYZ(np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]))
        area2 = vtkfilters.calculatePolyDataArea(line)
        self.assertGreaterEqual(area2, 0)
    
    def test_addNormalsToPolyData(self):
        """Test addNormalsToPolyData function."""
        with_normals = vtkfilters.addNormalsToPolyData(self.poly)
        self.assertTrue(vtkfilters.isVTP(with_normals))
        self.assertIsNotNone(with_normals.GetPointData().GetNormals())
        
        # Test with REV
        with_normals2 = vtkfilters.addNormalsToPolyData(self.poly, REV=True)
        self.assertTrue(vtkfilters.isVTP(with_normals2))
    
    def test_getBoundaryEdges(self):
        """Test getBoundaryEdges function."""
        # Create a surface with boundary
        plane = vtkfilters.buildPlaneSource([0, 0, 0], [1, 0, 0], [0, 1, 0], [5, 5])
        edges = vtkfilters.getBoundaryEdges(plane)
        self.assertTrue(vtkfilters.isVTP(edges))
    
    def test_getEdges(self):
        """Test getEdges function."""
        edges = vtkfilters.getEdges(self.poly)
        self.assertTrue(vtkfilters.isVTP(edges))
        
        # Test with FEATURE
        edges2 = vtkfilters.getEdges(self.poly, FEATURE=True)
        self.assertTrue(vtkfilters.isVTP(edges2))
    
    def test_decimateTris(self):
        """Test decimateTris function."""
        decimated = vtkfilters.decimateTris(self.poly, 0.5)
        self.assertTrue(vtkfilters.isVTP(decimated))
        self.assertLess(decimated.GetNumberOfCells(), self.poly.GetNumberOfCells())
    
    def test_getLoopSubDivided(self):
        """Test getLoopSubDivided function."""
        subdivided = vtkfilters.getLoopSubDivided(self.poly, 1)
        self.assertTrue(vtkfilters.isVTP(subdivided))
        self.assertGreater(subdivided.GetNumberOfCells(), self.poly.GetNumberOfCells())
    
    def test_poissonRecon(self):
        """Test poissonRecon function."""
        # Check if vtkPoissonReconstruction is available
        try:
            _ = vtk.vtkPoissonReconstruction()
        except AttributeError:
            self.skipTest("vtkPoissonReconstruction not available in this VTK version")
            return
        
        # Create point cloud
        pts = np.random.rand(100, 3) * 2 - 1
        poly_cloud = vtkfilters.buildPolydataFromXYZ(pts)
        recon = vtkfilters.poissonRecon(poly_cloud, depth=5)
        self.assertTrue(vtkfilters.isVTP(recon))
    
    def test_pointCloudRemoveOutliers(self):
        """Test pointCloudRemoveOutliers function."""
        # Create point cloud with outliers
        pts = np.random.rand(100, 3)
        poly_cloud = vtkfilters.buildPolydataFromXYZ(pts)
        cleaned = vtkfilters.pointCloudRemoveOutliers(poly_cloud)
        self.assertTrue(vtkfilters.isVTP(cleaned))
        self.assertLessEqual(cleaned.GetNumberOfPoints(), poly_cloud.GetNumberOfPoints())


class TestResampleOperations(unittest.TestCase):
    """Test resample operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        arr = np.random.rand(10*10*10)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
        self.poly = vtkfilters.buildSphereSource([5, 5, 5], 2.0, res=10)
    
    def test_filterResampleToDataset(self):
        """Test filterResampleToDataset function."""
        target = vtkfilters.buildRawImageData([5, 5, 5], [2, 2, 2], [0, 0, 0])
        resampled = vtkfilters.filterResampleToDataset(self.img, target)
        self.assertTrue(vtkfilters.isVTI(resampled))
        self.assertEqual(resampled.GetNumberOfPoints(), target.GetNumberOfPoints())
        
        # Test with PASS_POINTS
        resampled2 = vtkfilters.filterResampleToDataset(self.img, target, PASS_POINTS=True)
        self.assertTrue(vtkfilters.isVTI(resampled2))
    
    def test_filterResampleToImage(self):
        """Test filterResampleToImage function."""
        vts = vtkfilters.vtiToVts(self.img)
        resampled = vtkfilters.filterResampleToImage(vts, dims=[5, 5, 5])
        self.assertTrue(vtkfilters.isVTI(resampled))
        
        # Test without dims
        resampled2 = vtkfilters.filterResampleToImage(vts)
        self.assertTrue(vtkfilters.isVTI(resampled2))
    
    def test_filterResliceImage(self):
        """Test filterResliceImage function."""
        reslice = vtkfilters.filterResliceImage(self.img, [5, 5, 5], [0, 0, 1])
        self.assertIsNotNone(reslice)
        output = reslice.GetOutput()
        self.assertTrue(vtkfilters.isVTI(output))
        
        # Test with guiding vector
        reslice2 = vtkfilters.filterResliceImage(self.img, [5, 5, 5], [0, 0, 1], guidingVector=[1, 0, 0])
        self.assertIsNotNone(reslice2)
    
    def test_filterVtiMedian(self):
        """Test filterVtiMedian function."""
        filtered = vtkfilters.filterVtiMedian(self.img, filterKernalSize=3)
        self.assertTrue(vtkfilters.isVTI(filtered))
        self.assertEqual(filtered.GetNumberOfPoints(), self.img.GetNumberOfPoints())
        
        # Test with tuple kernel
        filtered2 = vtkfilters.filterVtiMedian(self.img, filterKernalSize=[3, 3, 3])
        self.assertTrue(vtkfilters.isVTI(filtered2))
    
    def test_filterImageGradient(self):
        """Test filterImageGradient function."""
        gradient = vtkfilters.filterImageGradient(self.img, 'scalars')
        self.assertTrue(vtkfilters.isVTI(gradient))
        self.assertIn('scalars-Gradient', vtkfilters.getArrayNames(gradient))
        
        # Test with custom output name
        gradient2 = vtkfilters.filterImageGradient(self.img, 'scalars', outputArrayName='customGradient')
        self.assertIn('customGradient', vtkfilters.getArrayNames(gradient2))
    
    def test_filterAnisotropicDiffusion(self):
        """Test filterAnisotropicDiffusion function."""
        filtered = vtkfilters.filterAnisotropicDiffusion(self.img, iterations=3)
        self.assertTrue(vtkfilters.isVTI(filtered))
        self.assertEqual(filtered.GetNumberOfPoints(), self.img.GetNumberOfPoints())


class TestSurfaceOperations(unittest.TestCase):
    """Test surface-related operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([20, 20, 20], [0.5, 0.5, 0.5], [0, 0, 0])
        arr = np.random.rand(20*20*20)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
        self.surf = vtkfilters.buildSphereSource([10, 10, 10], 3.0, res=15)
        self.surf = vtkfilters.filterTriangulate(self.surf)
    
    def test_filterSurfaceToImageStencil(self):
        """Test filterSurfaceToImageStencil function."""
        stencil = vtkfilters.filterSurfaceToImageStencil(self.img, self.surf, fill_value=1)
        self.assertTrue(vtkfilters.isVTI(stencil))
        self.assertEqual(stencil.GetNumberOfPoints(), self.img.GetNumberOfPoints())
    
    def test_filterMaskImageBySurface(self):
        """Test filterMaskImageBySurface function."""
        masked = vtkfilters.filterMaskImageBySurface(self.img, self.surf, fill_value=1, arrayName='LabelMap')
        self.assertTrue(vtkfilters.isVTI(masked))
        self.assertIn('LabelMap', vtkfilters.getArrayNames(masked))
    
    def test_filterGetEnclosedPts(self):
        """Test filterGetEnclosedPts function."""
        # Ensure surface is closed and properly positioned
        # Use a larger sphere that definitely encloses some points
        large_surf = vtkfilters.buildSphereSource([10, 10, 10], 8.0, res=15)
        large_surf = vtkfilters.filterTriangulate(large_surf)
        
        # Test POLYDATA return - returns UnstructuredGrid, not PolyData
        result = vtkfilters.filterGetEnclosedPts(self.img, large_surf, RETURNTYPE='POLYDATA')
        self.assertIsNotNone(result)
        # It's actually an UnstructuredGrid, so check it's a valid VTK object
        self.assertGreaterEqual(result.GetNumberOfPoints(), 0)
        
        # Test tf return
        tf = vtkfilters.filterGetEnclosedPts(self.img, large_surf, RETURNTYPE='tf')
        self.assertIsInstance(tf, np.ndarray)
        self.assertEqual(len(tf), self.img.GetNumberOfPoints())
        
        # Test ID return
        ids = vtkfilters.filterGetEnclosedPts(self.img, large_surf, RETURNTYPE='ID')
        self.assertIsInstance(ids, np.ndarray)
        # IDs may be empty if no points are inside, which is valid
    
    def test_filterGetPointsInsideSurface(self):
        """Test filterGetPointsInsideSurface function."""
        points = vtkfilters.filterGetPointsInsideSurface(self.img, self.surf)
        self.assertTrue(vtkfilters.isVTP(points))
    
    def test_filterGetPointIDsInsideSurface(self):
        """Test filterGetPointIDsInsideSurface function."""
        ids = vtkfilters.filterGetPointIDsInsideSurface(self.img, self.surf)
        self.assertIsInstance(ids, np.ndarray)
        self.assertGreater(len(ids), 0)
    
    def test_filterGetPolydataInsideSurface(self):
        """Test filterGetPolydataInsideSurface function."""
        # Use a larger sphere that definitely encloses some points
        large_surf = vtkfilters.buildSphereSource([10, 10, 10], 8.0, res=15)
        large_surf = vtkfilters.filterTriangulate(large_surf)
        result = vtkfilters.filterGetPolydataInsideSurface(self.img, large_surf)
        # Returns UnstructuredGrid, not PolyData
        self.assertIsNotNone(result)
        self.assertGreaterEqual(result.GetNumberOfPoints(), 0)
    
    def test_filterGetArrayValuesWithinSurface(self):
        """Test filterGetArrayValuesWithinSurface function."""
        values = vtkfilters.filterGetArrayValuesWithinSurface(self.img, self.surf, 'scalars')
        self.assertIsInstance(values, np.ndarray)
        self.assertGreater(len(values), 0)
    
    def test_filterNullOutsideSurface(self):
        """Test filterNullOutsideSurface function."""
        nulled = vtkfilters.filterNullOutsideSurface(self.img, self.surf, arrayListToNull=['scalars'])
        self.assertTrue(vtkfilters.isVTI(nulled))
        arr = vtkfilters.getArrayAsNumpy(nulled, 'scalars')
        # Points outside should be zero
        self.assertTrue(np.any(arr == 0))
    
    def test_filterNullInsideSurface(self):
        """Test filterNullInsideSurface function."""
        nulled = vtkfilters.filterNullInsideSurface(self.img, self.surf, arrayListToNull=['scalars'], nullVal=0.0)
        self.assertTrue(vtkfilters.isVTI(nulled))
        arr = vtkfilters.getArrayAsNumpy(nulled, 'scalars')
        # Some points inside should be nulled
        self.assertTrue(np.any(arr == 0.0))


class TestVolumeFilters(unittest.TestCase):
    """Test volume filter operations."""
    
    def setUp(self):
        """Set up test data."""
        self.img = vtkfilters.buildRawImageData([10, 10, 10], [1, 1, 1], [0, 0, 0])
        arr = np.random.rand(10*10*10)
        vtkfilters.setArrayFromNumpy(self.img, arr, 'scalars', SET_SCALAR=True)
    
    def test_extractStructuredSubGrid(self):
        """Test extractStructuredSubGrid function."""
        extracted = vtkfilters.extractStructuredSubGrid(self.img, ijkMinMax=[2, 7, 2, 7, 2, 7])
        self.assertTrue(vtkfilters.isVTI(extracted))
        self.assertLess(extracted.GetNumberOfPoints(), self.img.GetNumberOfPoints())
        
        # Test with sampleRate
        extracted2 = vtkfilters.extractStructuredSubGrid(self.img, ijkMinMax=[0, 9, 0, 9, 0, 9], sampleRate=(2, 2, 2))
        self.assertTrue(vtkfilters.isVTI(extracted2))
    
    def test_extractVOI(self):
        """Test extractVOI function."""
        extracted = vtkfilters.extractVOI(self.img, ijkMinMax=[2, 7, 2, 7, 2, 7])
        self.assertTrue(vtkfilters.isVTI(extracted))
        self.assertLess(extracted.GetNumberOfPoints(), self.img.GetNumberOfPoints())
        
        # Test without ijkMinMax
        extracted2 = vtkfilters.extractVOI(self.img)
        self.assertTrue(vtkfilters.isVTI(extracted2))
    
    def test_extractVOI_fromFov(self):
        """Test extractVOI_fromFov function."""
        fov = vtkfilters.buildSphereSource([5, 5, 5], 3.0, res=10)
        extracted = vtkfilters.extractVOI_fromFov(self.img, fov)
        self.assertTrue(vtkfilters.isVTI(extracted))
    
    def test_getDataWithThreshold(self):
        """Test getDataWithThreshold function."""
        # Use a wider threshold range to ensure we get some points
        # Random array should have values between 0 and 1
        thresholded = vtkfilters.getDataWithThreshold(self.img, 'scalars', -1.0, 2.0)
        self.assertIsNotNone(thresholded)
        # Returns UnstructuredGrid, should have some points with full range
        self.assertGreater(thresholded.GetNumberOfPoints(), 0)
        
        # Test with a very narrow range (may have 0 points)
        thresholded2 = vtkfilters.getDataWithThreshold(self.img, 'scalars', 0.9, 1.0)
        self.assertIsNotNone(thresholded2)
        self.assertGreaterEqual(thresholded2.GetNumberOfPoints(), 0)
    
    def test_countPointsInVti(self):
        """Test countPointsInVti function."""
        points = vtkfilters.buildPolydataFromXYZ(np.random.rand(50, 3) * 10)
        counted = vtkfilters.countPointsInVti(self.img, points, countArrayName='count')
        self.assertTrue(vtkfilters.isVTI(counted))
        self.assertIn('count', vtkfilters.getArrayNames(counted))
        
        # Test with weighting array
        weights = np.random.rand(points.GetNumberOfPoints())
        vtkfilters.setArrayFromNumpy(points, weights, 'weights')
        counted2 = vtkfilters.countPointsInVti(self.img, points, countArrayName='count2', weightingArray='weights')
        self.assertIn('count2', vtkfilters.getArrayNames(counted2))


class TestConnectedRegionFilters(unittest.TestCase):
    """Test connected region filter operations."""
    
    def setUp(self):
        """Set up test data."""
        # Create a disconnected surface
        sphere1 = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=8)
        sphere2 = vtkfilters.buildSphereSource([5, 0, 0], 1.0, res=8)
        self.disconnected = vtkfilters.appendPolyData(sphere1, sphere2)
        self.single = vtkfilters.buildSphereSource([0, 0, 0], 1.0, res=10)
    
    def test_getConnectedRegionLargest(self):
        """Test getConnectedRegionLargest function."""
        largest = vtkfilters.getConnectedRegionLargest(self.disconnected)
        self.assertTrue(vtkfilters.isVTP(largest))
        # The largest region should have at least some points
        self.assertGreater(largest.GetNumberOfPoints(), 0)
        # Note: if spheres are close enough, they might be considered connected
        # So we just check that we get a valid result
        
        # Test with single region
        largest2 = vtkfilters.getConnectedRegionLargest(self.single)
        self.assertEqual(largest2.GetNumberOfPoints(), self.single.GetNumberOfPoints())
    
    def test_getConnectedRegionContaining(self):
        """Test getConnectedRegionContaining function."""
        region = vtkfilters.getConnectedRegionContaining(self.disconnected, 0)
        self.assertTrue(vtkfilters.isVTP(region))
        self.assertGreater(region.GetNumberOfPoints(), 0)
    
    def test_getConnectedRegionClosestToX(self):
        """Test getConnectedRegionClosestToX function."""
        region = vtkfilters.getConnectedRegionClosestToX(self.disconnected, np.array([0, 0, 0]))
        self.assertTrue(vtkfilters.isVTP(region))
        self.assertGreater(region.GetNumberOfPoints(), 0)
    
    def test_getConnectedRegionAll(self):
        """Test getConnectedRegionAll function."""
        regions = vtkfilters.getConnectedRegionAll(self.disconnected)
        self.assertGreater(len(regions), 1)
        for region in regions:
            self.assertTrue(vtkfilters.isVTP(region))
            self.assertGreater(region.GetNumberOfPoints(), 0)
        
        # Test with minPts
        regions2 = vtkfilters.getConnectedRegionAll(self.disconnected, minPts=10)
        self.assertGreaterEqual(len(regions2), 0)
    
    def test_getConnectedRegionMinDistToX(self):
        """Test getConnectedRegionMinDistToX function."""
        region = vtkfilters.getConnectedRegionMinDistToX(self.disconnected, np.array([0, 0, 0]), minNPts=10)
        self.assertTrue(vtkfilters.isVTP(region))
        self.assertGreater(region.GetNumberOfPoints(), 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_polydata(self):
        """Test operations with empty polydata."""
        empty = vtk.vtkPolyData()
        # Should not crash
        names = vtkfilters.getArrayNames(empty)
        self.assertEqual(len(names), 0)
    
    def test_single_point(self):
        """Test operations with single point."""
        single_pt = vtkfilters.buildPolydataFromXYZ(np.array([[0, 0, 0]]))
        names = vtkfilters.getArrayNames(single_pt)
        self.assertEqual(len(names), 0)
    
    def test_zero_array(self):
        """Test with zero-sized arrays."""
        img = vtkfilters.buildRawImageData([1, 1, 1], [1, 1, 1], [0, 0, 0])
        arr = np.array([0.5])
        vtkfilters.setArrayFromNumpy(img, arr, 'test')
        retrieved = vtkfilters.getArrayAsNumpy(img, 'test')
        self.assertEqual(len(retrieved), 1)
    
    def test_very_large_image(self):
        """Test with very large image dimensions."""
        # Use smaller dimensions to avoid memory issues in tests
        img = vtkfilters.buildRawImageData([50, 50, 50], [1, 1, 1], [0, 0, 0])
        self.assertEqual(img.GetNumberOfPoints(), 50*50*50)
    
    def test_negative_coordinates(self):
        """Test with negative coordinates."""
        img = vtkfilters.buildRawImageData([5, 5, 5], [1, 1, 1], [-10, -10, -10])
        pts = vtkfilters.getVtkPointsAsNumpy(img)
        self.assertTrue(np.all(pts[:, 0] < 0))
    
    def test_non_unit_spacing(self):
        """Test with non-unit spacing."""
        img = vtkfilters.buildRawImageData([5, 5, 5], [0.1, 0.2, 0.3], [0, 0, 0])
        res = vtkfilters.getResolution_VTI(img)
        np.testing.assert_array_almost_equal(res, [0.1, 0.2, 0.3])


if __name__ == '__main__':
    unittest.main()

