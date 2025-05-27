"""
Basic Manim Animation Example

This is a simple example of Manim code that can be executed by the MCP server.
Copy this code and use it with the execute_manim tool.
"""

from manim import *

class BasicShapes(Scene):
    def construct(self):
        # Create some basic shapes
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED)
        triangle = Triangle(color=GREEN)
        
        # Position them
        square.shift(LEFT * 3)
        triangle.shift(RIGHT * 3)
        
        # Animate them
        self.play(Create(circle))
        self.play(Create(square), Create(triangle))
        self.play(
            circle.animate.shift(UP * 2),
            square.animate.rotate(PI/4),
            triangle.animate.scale(1.5)
        )
        self.wait(1)
        
        # Transform circle into square
        self.play(Transform(circle, Square(side_length=2, color=YELLOW).shift(UP * 2)))
        self.wait(1) 