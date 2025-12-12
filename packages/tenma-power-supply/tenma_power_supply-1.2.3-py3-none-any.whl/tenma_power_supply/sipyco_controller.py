from generic_scpi_driver import get_controller_func

from .driver import TENMAPowerSupply

main = get_controller_func("TENMAPowerSupply", 3301, TENMAPowerSupply)


if __name__ == "__main__":
    main()
