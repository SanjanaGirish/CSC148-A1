  # Madhav's Move function for Recycling Bin
  def move(self, direction: Tuple[int, int]) -> bool:
        """Move this recycling bin to tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return whether or not this move was successful.
        If the new tile is occupied by another RecyclingBin, push
        that RecyclingBin one tile away in the same direction and take
        its tile (as described in the Assignment 1 handout).
        If the new tile is occupied by any other Character or if it
        is beyond the boundaries of the board, do nothing and return False.
        Precondition:
        direction in DIRECTIONS
        >>> b = GameBoard(4, 2)
        >>> rb = RecyclingBin(b, 0, 0)
        >>> rb.move(UP)
        False
        >>> rb.move(DOWN)
        True
        >>> b.at(0, 1) == [rb]
        True
        """
        # TODO Task #2
        if self.x + direction[0] >= self.board.width or self.y + direction[1] \
                >= self.board.height:
            return False
        # If the target spot is not occupied
        if len(self.board.at(self.x +
                             direction[0], self.y + direction[1])) == 0:
            self.x += direction[0]
            self.y += direction[1]
            return True
        # If the target spot contains a nonempty GarbageCan
        if len(self.board.at(self.x +
                             direction[0], self.y + direction[1])) == 2:
            return False
        # If the target spot consists of one character thats not a recycling bin
        if not isinstance(self.board.at(self.x +
                                        direction[0], self.y + direction[1])[0],
                          RecyclingBin):
            return False
        # Finally, if the target spot contains a recycling bin:
        if self.board.at(self.x + direction[0],
                         self.y + direction[1])[0].move(direction):
            self.x += direction[0]
            self.y += direction[1]
            return True
        else:
            return False
