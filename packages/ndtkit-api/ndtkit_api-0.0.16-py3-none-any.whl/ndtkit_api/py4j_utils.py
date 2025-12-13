from .ndtkit_socket_connection import gateway


def to_java_list(py_list):
    java_list = gateway.jvm.java.util.ArrayList()
    for item in py_list:
        java_list.add(item)
    return java_list
