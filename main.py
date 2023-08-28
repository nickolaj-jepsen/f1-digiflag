from f1_unicorn import main
import uasyncio


if __name__ == "__main__":
    loop = uasyncio.get_event_loop()
    task = loop.create_task(main())
    loop.run_forever()
