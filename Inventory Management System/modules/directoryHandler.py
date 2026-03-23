import os
def base_path():
    # ------------------ BASE PATH SETUP ------------------
    BASE_DIR = os.path.dirname(".")
    #print(BASE_DIR)
    return BASE_DIR
    # ---------------------------------------------------

def module_path():
    module_DIR = os.path.dirname(os.path.abspath(__file__))
    return module_DIR

def image_path():
    BASE_DIR = base_path()
    IMAGE_DIR = os.path.join(BASE_DIR, "images")

    os.makedirs(IMAGE_DIR, exist_ok=True)

    return IMAGE_DIR

def bill_path():
    BASE_DIR = base_path()
    BILL_DIR = os.path.join(BASE_DIR, "bill")

    os.makedirs(BILL_DIR, exist_ok=True)

    return BILL_DIR

def database_path():
    BASE_DIR = base_path()
    DB_DIR = os.path.join(BASE_DIR, "database")
    os.makedirs(DB_DIR, exist_ok=True)
    return DB_DIR