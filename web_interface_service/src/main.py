from . import interface, config


if __name__ == '__main__':
    interface.demo.launch(server_name="0.0.0.0", server_port=config.SERVICE_PORT)
    