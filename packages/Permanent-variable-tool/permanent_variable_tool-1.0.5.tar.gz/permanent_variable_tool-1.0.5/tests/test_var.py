import os 
import sys
import unittest 
import pvt
sys.path.insert(0,  os.path.dirname(os.path.abspath(__file__))) 
class TestVar(unittest.TestCase):
    def setUp(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
        self.data_dir = os.path.join(self.current_dir,  'data')
        if not os.path.exists(self.data_dir): 
            os.makedirs(self.data_dir) 
        self.original_cwd  = os.getcwd() 
        os.chdir(self.current_dir) 
    def tearDown(self):
        os.chdir(self.original_cwd) 
        test_files = ['test_var.var',  'empty_var.var',  'number_var.var',  
                     'existing_var.var',  'read_test.var',  'delete_test.var', 
                     'workflow_var.var',  'unicode_var.var',  'large_var.var'] 
        for filename in test_files:
            file_path = os.path.join(self.data_dir,  filename)
            if os.path.exists(file_path): 
                try:
                    os.remove(file_path) 
                except:
                    pass
    def test_new_create_file_with_value(self):
        pvt.new('test_var', 'hello world')
        file_path = os.path.join(self.data_dir,  'test_var.var') 
        self.assertTrue(os.path.exists(file_path)) 
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read() 
        self.assertEqual(content,  'hello world')
    def test_new_create_file_empty_value(self):
        pvt.new('empty_var')
        file_path = os.path.join(self.data_dir,  'empty_var.var') 
        self.assertTrue(os.path.exists(file_path)) 
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read() 
        self.assertEqual(content,  '')
    def test_new_create_file_numeric_value(self):
        pvt.new('number_var', 123)
        file_path = os.path.join(self.data_dir,  'number_var.var') 
        self.assertTrue(os.path.exists(file_path)) 
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read() 
        self.assertEqual(content,  '123')
    def test_new_overwrite_existing_file(self):
        pvt.new('existing_var', 'old value')
        file_path = os.path.join(self.data_dir,  'existing_var.var') 
        pvt.new('existing_var', 'new value')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read() 
        self.assertEqual(content,  'new value')
    def test_read_existing_file(self):
        pvt.new('read_test', 'test content')
        content = pvt.read('read_test')
        self.assertEqual(content,  'test content')
    def test_read_empty_file(self):
        pvt.new('empty_read')
        content = pvt.read('empty_read')
        self.assertEqual(content,  '')
    def test_read_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError)  as context:
            pvt.read('nonexistent_var')
        self.assertIn("Variable  file' nonexistent_var.var'  does not exist", str(context.exception)) 
    def test_delete_existing_file(self):
        pvt.new('delete_test', 'to be deleted')
        file_path = os.path.join(self.data_dir,  'delete_test.var') 
        self.assertTrue(os.path.exists(file_path)) 
        pvt.delete('delete_test')
        self.assertFalse(os.path.exists(file_path)) 
    def test_delete_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError)  as context:
            pvt.delete('nonexistent_var') 
        self.assertIn("Variable  file' nonexistent_var.var'  does not exist", str(context.exception)) 
    def test_integration_workflow(self):
        pvt.new('workflow_var', 'integration test')
        file_path = os.path.join(self.data_dir,  'workflow_var.var') 
        self.assertTrue(os.path.exists(file_path)) 
        content = pvt.read('workflow_var')
        self.assertEqual(content,  'integration test')
        pvt.delete('workflow_var')
        self.assertFalse(os.path.exists(file_path)) 
        with self.assertRaises(FileNotFoundError): 
            pvt.read('workflow_var')
    def test_unicode_content(self):
        unicode_content = '中文测试 Unicode characters: ñáéíóú'
        pvt.new('unicode_var', unicode_content)
        content = pvt.read('unicode_var')
        self.assertEqual(content,  unicode_content)
    def test_large_content(self):
        large_content = 'x' * 1000
        pvt.new('large_var', large_content)
        content = pvt.read('large_var')
        self.assertEqual(content,  large_content)
        self.assertEqual(len(content),  1000)
def run_simple_test():
    current_dir = os.path.dirname(os.path.abspath(__file__)) 
    data_dir = os.path.join(current_dir,  'data')
    if not os.path.exists(data_dir): 
        os.makedirs(data_dir) 
    original_cwd = os.getcwd() 
    os.chdir(current_dir) 
    try:
        pvt.new('simple_test', 'hello world')
        file_path = os.path.join(data_dir,  'simple_test.var') 
        assert os.path.exists(file_path),  "Error"
        content = pvt.read('simple_test')
        assert content == 'hello world', "Error"
        pvt.delete('simple_test')
        assert not os.path.exists(file_path),  "Error"
        try:
            pvt.read('nonexistent_simple')
            assert False, "Error"
        except FileNotFoundError:
            print("",end= "")
    except Exception as e:
        print("Error")
        raise 
    finally:
        os.chdir(original_cwd) 
        test_file = os.path.join(data_dir,  'simple_test.var') 
        if os.path.exists(test_file): 
            try:
                os.remove(test_file) 
            except:
                pass 
if __name__ == '__main__':
    unittest.main(verbosity=2) 