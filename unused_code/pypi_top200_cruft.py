import scene
ui = scene.ui

# pip_loc is a tuple of lists of tuples.  Use tuples where possible because
# lists require slightly more RAM.  For each domino die from 0 to 9 there is a
# list of the coordinates of the dots/pips.
pip_locs = ([()], [(1, 1)], [(0, 0), (2, 2)], [(0, 0), (1, 1), (2, 2)], [(
    0, 0), (2, 0), (0, 2), (2, 2)], [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
            [(0, 0), (1, 0), (2, 0), (0, 2), (1, 2),
             (2, 2)], [(0, 0), (1, 0), (2, 0), (1, 1), (0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 0), (2, 0), (0, 1), (2, 1), (0, 2), (1, 2),
             (2, 2)], [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2),
                       (1, 2), (2, 2)])


def generateDominosYield(inMaxDie=6):  # Yield = Generator -- is an iterator
    for x in range(inMaxDie + 1):
        for y in range(inMaxDie + 1):
            if x <= y:
                yield (x, y)


def domino_image(pips=(5, 6), die_size=70, fg_color='blue', bg_color='grey'):
    width = die_size * 2
    height = die_size
    with ui.ImageContext(width, height) as ctx:
        # domino is rounded rect in background color
        ui.set_color(bg_color)
        ui.Path.rounded_rect(0, 0, width, height, height / 10).fill()
        # pips are circles in foreground color
        ui.set_color(fg_color)
        pip_size = height / 3
        b = int(height / 14)
        wh = pip_size - 2 * b
        # draw pips[0]
        for loc in pip_locs[pips[0]]:
            if loc:
                x, y = loc
                ui.Path.oval(x * pip_size + b, y * pip_size + b, wh, wh).fill()
        # draw dividing line
        path = ui.Path()
        # path.line_width = 4
        path.move_to(die_size, b)
        path.line_to(die_size, height - b)
        path.close()
        path.stroke()
        # draw pips[1]
        for loc in pip_locs[pips[1]]:
            if loc:
                x, y = loc
                ui.Path.oval(x * pip_size + b + die_size, y * pip_size + b, wh,
                             wh).fill()
        return scene.Texture(ctx.get_image())


class MyScene(scene.Scene):
    def setup(self):
        bufferSize = 4
        maxDie = 6
        dieSize = int((self.bounds.w - bufferSize * maxDie) / 14)
        top = int((self.bounds.h - bufferSize * maxDie) / 7)
        w = dieSize * 2
        h = dieSize
        for (i, j) in generateDominosYield(maxDie):
            theDomino = self.make_domino(pips=(i, j), die_size=dieSize)
            theDomino.position = (j * (w + bufferSize) + dieSize,
                                  top + i * (h + bufferSize))
        self.dragging_domino = None

    def make_domino(self, pips=(5, 6), die_size=70):
        image = domino_image(pips=pips, die_size=die_size)
        return scene.SpriteNode(image, parent=self,
                                position=self.bounds.center())

    def touch_began(self, touch):
        for domino in self.children:
            if touch.location in domino.frame:
                self.dragging_domino = domino
                return
        self.dragging_domino = None

    def touch_moved(self, touch):
        if self.dragging_domino:
            self.dragging_domino.position = touch.location

    def touch_ended(self, touch):
        self.dragging_domino = None


if __name__ == '__main__':
    scene.run(MyScene(), show_fps=False)
