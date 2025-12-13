#define PY_SSIZE_T_CLEAN
#include <Python.h>

/* --- 1. Define the C Struct for our Object --- */
typedef struct
{
  PyObject_HEAD
      // We will use a Python List internally for simplicity in this example,
      // but typically you would use a raw C linked list or array here for O(1).
      PyObject *data;
} QueueObject;

/* --- 2. Deallocation (Destructor) --- */
static void Queue_dealloc(QueueObject *self)
{
  Py_XDECREF(self->data); // Decrement reference count of list
  Py_TYPE(self)->tp_free((PyObject *)self);
}

/* --- 3. Initialization (__init__) --- */
static int Queue_init(QueueObject *self, PyObject *args, PyObject *kwds)
{
  self->data = PyList_New(0); // Create a new empty list
  if (self->data == NULL)
    return -1;
  return 0;
}

/* --- 4. Method: enqueue --- */
static PyObject *Queue_enqueue(QueueObject *self, PyObject *args)
{
  PyObject *item;
  // Parse arguments: "O" means we expect one generic Python Object
  if (!PyArg_ParseTuple(args, "O", &item))
  {
    return NULL;
  }
  // Append to our internal list
  if (PyList_Append(self->data, item) < 0)
  {
    return NULL;
  }
  Py_RETURN_NONE; // Return None in Python
}

/* --- 5. Method: dequeue --- */
static PyObject *Queue_dequeue(QueueObject *self, PyObject *Py_UNUSED(ignored))
{
  // Check if empty
  if (PyList_Size(self->data) == 0)
  {
    PyErr_SetString(PyExc_IndexError, "dequeue from empty queue");
    return NULL;
  }
  // Get item at index 0
  PyObject *item = PyList_GetItem(self->data, 0);
  Py_INCREF(item); // Increment ref because SetSlice will steal/delete it

  // Remove index 0 (this is O(n) for list, a real C queue would be O(1))
  if (PySequence_DelItem(self->data, 0) < 0)
  {
    Py_DECREF(item);
    return NULL;
  }
  return item;
}

/* --- 6. Method Definitions --- */
static PyMethodDef Queue_methods[] = {
    {"enqueue", (PyCFunction)Queue_enqueue, METH_VARARGS, "Add an item to the queue"},
    {"dequeue", (PyCFunction)Queue_dequeue, METH_NOARGS, "Remove an item from the queue"},
    {NULL} /* Sentinel */
};

/* --- 7. Type Definition --- */
static PyTypeObject QueueType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "opencp.backend.c_queue.FastQueue",
    .tp_doc = "A fast queue implemented in C",
    .tp_basicsize = sizeof(QueueObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)Queue_init,
    .tp_dealloc = (destructor)Queue_dealloc,
    .tp_methods = Queue_methods,
};

/* --- 8. Module Definition --- */
static struct PyModuleDef c_queue_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "c_queue",
    .m_doc = "C implementation of Queue",
    .m_size = -1,
};

/* --- 9. Module Initialization Function --- */
PyMODINIT_FUNC PyInit_c_queue(void)
{
  PyObject *m;
  if (PyType_Ready(&QueueType) < 0)
    return NULL;

  m = PyModule_Create(&c_queue_module);
  if (m == NULL)
    return NULL;

  Py_INCREF(&QueueType);
  if (PyModule_AddObject(m, "FastQueue", (PyObject *)&QueueType) < 0)
  {
    Py_DECREF(&QueueType);
    Py_DECREF(m);
    return NULL;
  }
  return m;
}