from app.application import Application
from render.graphic import Graphic

if __name__ == '__main__':
    application = Application()
    renderer = Graphic(application)
    while application.step():
        renderer.render()

    renderer.render()
