#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <kraken.h>
#include <memory>
#include <vector>

static PyObject *decompress(PyObject *self, PyObject *args) {
	byte *src;
	Py_ssize_t src_len;
	Py_ssize_t dst_len;
	if (!PyArg_ParseTuple(args, "y#n", &src, &src_len, &dst_len)) {
		PyErr_SetString(PyExc_TypeError, "Invalid parameters");
		return NULL;
	}

	auto dst = std::make_unique<uint8_t[]>(dst_len);

	// printf("src_len=%d, dst_len=%d\n", src_len, dst_len);

	int ret = Kraken_Decompress(src, src_len, dst.get(), dst_len);

	if (ret == -1) {
		PyErr_SetString(PyExc_ValueError, "Unable to decompress");
		return NULL;
	}

	if (ret != dst_len) {
		PyErr_SetString(PyExc_ValueError, "Decompressed size mismatch");
		return NULL;
	}

	PyObject *pbo = PyBytes_FromStringAndSize(NULL, dst_len);
	char *bytebuffer = PyBytes_AsString(pbo);

	for (int i = 0; i < dst_len; i++) {
		bytebuffer[i] = dst[i];
	}

	return pbo;

	// PyObject* py_dst_list = PyList_New(dst_len);

	// for (int i=0; i<dst_len; i++) {
	//     printf("byte%d=%d\n", i, dst[i]);
	//     PyList_Append(py_dst_list, PyLong_FromLong(dst[i]));
	// }
	// return py_dst_list;
}

static PyMethodDef methods[] = {
	{"decompress", (PyCFunction)decompress, METH_VARARGS, NULL},
	{NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT, "kraken_decompressor", NULL, -1, methods,
};

PyMODINIT_FUNC PyInit_kraken_decompressor(void) { return PyModule_Create(&module); }
