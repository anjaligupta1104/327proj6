import sys
from board import Board
from player import playerFactory
from memento import Memento

import tkinter as tk
from tkinter import messagebox

class SantoriniGUI():
    """Display board and options"""
    def __init__(self):
        self._window = tk.Tk()
        self._window.title("Santorini")
        self._window.geometry("5000x5000")

if __name__ == "__main__":
    obj = SantoriniGUI()