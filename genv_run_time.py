import os
import json
import logging
logging.basicConfig(level=logging.DEBUG)

def manage_docker_daemon_file():
    file_path = "/etc/docker/daemon.json"
    home_path = os.path.expanduser("~")
    json_content = {
        "runtimes": {
            "genv": {
                "path": "{}/genv/genv-docker/genv-container-runtime.py".format(home_path)
            }
        }
    }

    if not os.path.exists(file_path):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write JSON content to the file
        with open(file_path, 'w') as file:
            json.dump(json_content, file, indent=4)
        logging.info(f"File created and JSON content written to {file_path}")
    else:
        # Read and print the content of the file
        with open(file_path, 'r+') as file:
            try:
                content = json.load(file)
                logging.info(f"Content of {file_path}:\n{json.dumps(content, indent=4)}")

                # Check if the "runtimes" key exists
                if "runtimes" in content:
                    logging.info('The key "runtimes" exists in the JSON content.')
                    content['runtimes']['genv'] = {"path":"{}/genv/genv-docker/genv-container-runtime.py".format(home_path)}
                    logging.info("Genv docker runtime add {}".format(content))
                else:
                    content['runtimes']={}
                    content['runtimes']['genv'] = {"path":"{}/genv/genv-docker/genv-container-runtime.py".format(home_path)}
                    logging.info("Genv docker runtime add {}".format(content))
                file.seek(0)
                file.truncate()
                json.dump(content, file, indent=4)
            except json.JSONDecodeError:
                logging.info(f"Error: The file {file_path} does not contain valid JSON.")

# Call the function
manage_docker_daemon_file()
