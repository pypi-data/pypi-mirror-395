import os

# Method to delete any files that are expected to be debris from a given list
def cleanup_folder(action_path, del_list=[]):

    # Loop through the del list and remove any files that are found in 
    for file in del_list:
        target_path = os.path.join(action_path, file)
        if os.path.exists(target_path):
            print("File {} found from del list, removing...".format(file))
            try:
                os.remove(target_path)
                print("File remove successfully")
            except Exception as e:
                print("Failed to remove file: {}".format(e))
    
    # Flag to the user that the del list has been completed
    print("Excess files removed")