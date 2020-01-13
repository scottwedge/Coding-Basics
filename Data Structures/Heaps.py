import numpy as np


class N_ary_heap:
    
    def __init__(self, capacity, heap_type='min', overflow_off='head', dtype=float, n_ary=2):
        """
        Create an empty heap.
        
        Args:
            capacity (int, NoneType, optional): The capacity of the new array. None is interpreted as the size of array. Defaults to None.
            heap_type (str, optional): The type of heap to be made, either 'min' or 'max'. Defaults to 'min'.
            overflow_off (str, optional): Determines what to discard when values are pushed when the heap is at capacity, either 'head' or 'tail'. Defaults to 'head'.
            dtype (type, optional): The dtype of the heap. Defaults to float.
            n_ary (int, optional): The maximum number of children for each node, or the branching factor of the tree. Defaults to 2.
            
        Raises:
            TypeError: Raised if capacity is not of type int.
            ValueError: Raised if capacity is not positive.
            ValueError: Raised if heap_type is not 'min' or 'max'.
            TypeError: Raised if overflow_off is not of type str.
            ValueError: Raised if overflow_off is not 'head' or 'tail'.
            TypeError: Raised if dtype is not a type.
            TypeError: Raised if n_ary is not of type int.
            ValueError: Raised if n_ary is not positive.
        """

        # Validate inputs.

        # Validate capacity.
        if not isinstance(capacity, int):
            raise TypeError(f"capacity must be of type int.\n"
                            f"type(capacity): {type(capacity)}.")
        if capacity < 1:
            raise ValueError(f"capacity must be positive.\n"
                            f"capacity: {capacity}.")

        # Validate heap_type.
        if heap_type not in ['min', 'max']:
            raise ValueError(f"heap_type must be either 'min' or 'max'.\n"
                             f"heap_type: {heap_type}.")

        # Validate overflow_off.
        if not isinstance(overflow_off, str):
            raise TypeError(f"overflow_off must be of type str.\n"
                            f"type(overflow_off): {type(overflow_off)}.")
        if overflow_off not in ['head', 'tail']:
            raise ValueError(f"overflow_off must be either 'head' or 'tail'.\n"
                             f"overflow_off: {overflow_off}.")

        # Validate dtype.
        if not isinstance(dtype, type):
            raise TypeError(f"dtype must be a type.\n"
                            f"type(dtype): {type(dtype)}.")

        # Validate n_ary.
        if not isinstance(n_ary, int):
            raise TypeError(f"n_ary must be of type int.\n"
                            f"type(n_ary): {type(n_ary)}.")
        if n_ary < 1:
            raise ValueError(f"n_ary must be at least 1.\n"
                            f"n_ary: {n_ary}.")

        # Set attributes.

        self._heap_type = heap_type
        self._heap_array = np.full(capacity, np.nan, dtype)
        self._n_ary = n_ary
        self._size = 0


    def _is_more_extreme(self, challenger, incumbent):
        """Return True if challenger is more extreme than incumbent in the direction indicated by self._heap_type, else return False."""

        if self._heap_type == 'min':
            return challenger < incumbent
        elif self._heap_type == 'max':
            return challenger > incumbent
        else:
            raise RuntimeError(f"self._heap_type must be either 'min' or 'max'.\n"
                               f"self._heap_type: {self._heap_type}.")


    def _get_parent(self, child_index):
        """Returns the index for the parent of the child at child_index."""

        return (child_index - 1) // self._n_ary


    def _get_child(self, this_index, child_number=0, assume_correct=False):
        """Returns the index for the child_number-th child of the node at this_index."""

        return self._n_ary * this_index + child_number + 1
    

    def _get_min_or_max_child(self, this_index, min_or_max='min'):
        """
        If min_or_max == 'min': return the index for the smallest child of the node at this_index. 
        If min_or_max == 'max': return the index for the  largest child of the node at this_index. 
        
        If this is a leaf node, return None."""

        left_child_index = self.get_child(this_index)
        if left_child_index >= self._size:
            # The node at this_index is a leaf node.
            return None

        # Initially assume that the first child is the extremum.
        extremum_index = left_child_index
        extremum_value = self._heap_array[left_child_index]

        # Check the rest of the children for extremum candidates.
        for child_index in range(left_child_index + 1, left_child_index + self._n_ary):
            # Set extremum to the most extreme value among this node and its children in one direction, 
            # preferring small values if min_or_max == 'min' or else large ones if min_or_max == 'max'.

            if child_index >= self._size:
                # There are no more children of the node at this_index in the heap.
                return extremum_index

            # Update extremum if this child is more extreme.
            child_value = self._heap_array[child_index]
            if self._is_more_extreme(child_value, extremum_value):
                extremum_index = child_index
                extremum_value = child_value
        # End for-loop over children.

        return extremum_index


    def _exchange_values(self, index_x, index_y):
        """Exchange the values at index_x and index_y."""

        self._heap_array[index_x], self._heap_array[index_y] = self._heap_array[index_y], self._heap_array[index_x]

        
    def _sift_up(self, this_index):
        """Exchange the value at <this_index> with its predecessors in the tree until it satisfies the appropriate heap property."""
        
        # Traverse up the heap updating this_index with its children until it is set to the root, 
        # or is at least as extreme as its children (in the appropriate direction given self._heap_type).
        while True:
            
            this_value = self._heap_array[this_index]
            parent_index = get_parent(this_index)
            parent_value = self._heap_array[parent_index]
            # Note: the parent of the root is calculated as the root.
            # Having the same value as its 'parent', the heap property will be satisfied when this_index indicates the root (index 0).

            # Check whether parent_value is at least as extreme as this_value.
            if not self._is_more_extreme(this_value, parent_value):
                # The heap property is satisfied.
                return

            # The heap property is not yet satisfied.
            # Exchange this_value with parent_value and update this_index to parent_index.
            self._exchange_values(this_index, parent_index)
            this_index = parent_index


    # TODO: remove.
    def _sift_up_recursive(self, this_index):
        """Recursively exchange the value at this_index with its predecessors in the tree until it satisfies the appropriate heap property."""
        
        this_value = self._heap_array[this_index]
        parent_index = get_parent(this_index)
        parent_value = self._heap_array[parent_index]

        exchange_and_recurse = False
        if self._heap_type == 'min':
            if parent_value > this_value:
                exchange_and_recurse = True
        elif self._heap_type == 'max':
            if parent_value < this_value:
                exchange_and_recurse = True
        else:
            raise ValueError(f"self._heap_type must be either 'min' or 'max'.\n"
                             f"self._heap_type: {self._heap_type}.")
        
        if exchange_and_recurse:
            # Exchange this_value with parent_value.
            self._exchange_values(this_index, parent_index)
            self.sift_up(parent_index)
    
    
    def _sift_down(self, this_index):
        """Exchange the value at this_index with its descendents in the tree until it satisfies the appropriate heap property."""

        # Traverse down the heap updating this_index with its children until it is set to a leaf, 
        # or is at least as extreme as its children (in the appropriate direction given self._heap_type).
        while True:

            this_value = self._heap_array[this_index]
            extremum_child_index = self._get_min_or_max_child(this_index, min_or_max=self._heap_type)

            # Check whether the heap property has been satisfied, and 
            # if extremum_child_index is not None, set extremum_child_value.

            if extremum_child_index is None:
                # The node at this_index is a leaf node, satisfying the heap property.
                return

            # extremum_child_index is a valid index. Set extremum_child_value.
            extremum_child_value = self._heap_array[extremum_child_index]

            # Check whether this_value is at least as extreme as extreme_child_value.
            if not self._is_more_extreme(extremum_child_value, this_value):
                # The heap property is satisfied.
                return

            # The heap property is not yet satisfied.
            # Exchange this_value with extremum_child_value and update this_index to extremum_child_index.
            self._exchange_values(this_index, extremum_child_index)
            this_index = extremum_child_index


    # TODO: remove.
    def _sift_down_recursive(self, this_index):
        """Recursively exchange the value at this_index with its descendents in the tree until it satisfies the appropriate heap property."""

        this_value = self._heap_array[this_index]
        extremum_child_index = self._get_min_or_max_child(this_index, min_or_max=self._heap_type)

        # Check for completion.

        if extremum_child_index is None:
            # The node at this_index is a leaf node.
            return
        extremum_child_value = self._heap_array[extremum_child_index]
        # Check whether this_value is at least as extreme as extreme_child_value.
        if self._heap_type == 'min':
            if this_value <= extremum_child_value:
                return
        elif self._heap_type == 'max':
            if this_value >= extremum_child_value:
                return
        else:
            raise ValueError(f"self._heap_type must be either 'min' or 'max'.\n"
                             f"self._heap_type: {self._heap_type}.")
        # The appropriate heap property is not satisfied.

        # Exchange and recurse.
        self._exchange_values(this_index, extremum_child_index)
        self.sift_down_recursive(extremum_child_index)
    

    def _force_overflow(self, num_overflow):
        """Force the overflow of up to num_overflow nodes."""

        # Validate inputs.
        if not isinstance(num_overflow, int):
            raise TypeError(f"num_overflow must be of type int.\n"
                            f"type(num_overflow): {type(num_overflow)}.")
        if num_overflow < 1:
            raise ValueError(f"num_overflow must be positive.\n"
                            f"num_overflow: {num_overflow}.")
        if num_overflow > self.size():
            raise RuntimeError(f"num_overflow must not exceed the current size of the heap.\n"
                               f"num_overflow: {num_overflow}, self.size(): {self.size()}.")

        if self._overflow_off == 'head':
            for _ in range(min(self.size(), num)):
                self.pop()
        elif self._overflow_off == 'tail':
            self.poll(num_overflow)
        else:
            raise ValueError(f"overflow_off must be either 'head' or 'tail'.\n"
                                 f"overflow_off: {overflow_off}.")

'''
  _    _                         __  __          _     _                   _       
 | |  | |                       |  \/  |        | |   | |                 | |      
 | |  | |  ___    ___   _ __    | \  / |   ___  | |_  | |__     ___     __| |  ___ 
 | |  | | / __|  / _ \ | '__|   | |\/| |  / _ \ | __| | '_ \   / _ \   / _` | / __|
 | |__| | \__ \ |  __/ | |      | |  | | |  __/ | |_  | | | | | (_) | | (_| | \__ \
  \____/  |___/  \___| |_|      |_|  |_|  \___|  \__| |_| |_|  \___/   \__,_| |___/
                                                                                   
                                                                                   
'''

    def heapsort(self, min_or_max_first=None):
        """
        Performs heapsort in place and returns a copy of the sorted array, possibly reversed based on min_or_max_first.
        
        Args:
            min_or_max_first (bool, NoneType, optional): Determines whether the returned array is ascending or descending. 
            If None, the heap_type is assumed. Does not affect the resultant state of the underlying heap. Defaults to None.
        """

        # Validate min_or_max_first.
        if not isinstance(min_or_max_first, (str, NoneType)):
            raise TypeError(f"min_or_max_first must be of type str or NoneType.\n"
                            f"type(min_or_max_first): {type(min_or_max_first)}.")
        if min_or_max_first not in ['min', 'max', None]:
            raise ValueError(f"min_or_max_first must be either 'min', 'max', or None.\n"
                             f"min_or_max_first: {min_or_max_first}.")
        if min_or_max_first is None:
            min_or_max_first = self._heap_type

        # Sort in self._heap_type-last order.
        actual_size = self._size
        while not self.is_empty():
            self._exchange_values(0, self._size - 1)
            self._size -= 1
            self._sift_down(0)
        self._size = actual_size
        
        if min_or_max_first != self._heap_type:
            output = np.copy(self._heap_array[:self._size])
        
        # Restore heap property.
        self._heap_array[:self._size] = np.flip(self._heap_array[:self._size])

        if min_or_max_first == self._heap_type:
            output = np.copy(self._heap_array[:self._size])
        
        return output


    def size(self):
        """
        Returns the size of the heap, i.e. the number of stored values.
        
        Returns:
            int: The number of values currently stored in the heap.
        """

        return self._size


    def is_empty(self):
        """
        Returns True if there are no elements in the heap, else False.
        
        Returns:
            bool: True if empty, False if not empty.
        """

        return self._size == 0
        

    def pop(self):
        """
        Gracefully removes and returns the root. If the heap is empty, returns None.
        
        Returns:
            dtype: The root of the heap, or None if the heap is empty.
        """

        if self.is_empty():
            return None
        
        root = self._heap_array[0]

        # Exchange the root with the last item in the heap, 
        # remove it from the heap by decrementing size, 
        # and restore the heap property.
        self._exchange_values(0, self._size - 1)
        self._size -= 1
        self._sift_down(0)

        return root


    def replace(self, new_value):
        """
        Replaces the root with new_value and sifts it down. Returns the old root.
        
        Args:
            new_value (dtype): The value to be inserted.
        
        Returns:
            dtype: The root at insertion time.
        """

        if self.is_empty():
            root = None
            self.push(new_value)
        else:
            root = self._heap_array[0]
            # Override the value at the root and restore the heap property.
            self._heap_array[0] = new_value
            self._sift_down(0)
        
        return root
    

    def peek(self):
        """
        If there are values in the heap, return values starting at the root. 
        If the heap is empty, return None.

        Returns:
            (dtype, NoneType): The root value with the type specified at initialization (default float), or None.
        """

        if self._size == 0:
            return None
        else:
            return self._heap_array[0]


    def peek_tail(self, num_peek=1, unpack_single=True, tail_first=True):
        """
        If the heap is empty, return None. Otherwise, 
        perform heapsort in place with self._heap_type at the root, 
        then returns the last item or items in the heap.

        Args:
            num_peek (int): The number of values to peek, minimum 1. Defaults to 1.
            unpack_single (bool): If True and num_peek == 1, then return the single value rather than a list. Defaults to True.
            tail_first (bool): If True, returns values in tail-first order, else in sorted order. Defaults to True.
        
        Returns:
            dtype, list, NoneType: The tail of the sorted self._heap_array.
        """

        # Validate inputs.
        if not isinstance(num_peek, int):
            raise TypeError(f"num_peek must be of type int.\n"
                            f"type(num_peek): {type(num_peek)}.")
        if num_peek < 1:
            raise ValueError(f"num_peek must be positive.\n"
                            f"num_peek: {num_peek}.")
        if num_peek > self.size():
            raise RuntimeError(f"num_peek must not exceed the current size of the heap.\n"
                               f"num_peek: {num_peek}, self.size(): {self.size()}.")

        if self.is_empty():
            return None

        self.heapsort()

        if unpack_single and num_peek == 1:
            return self._heap_array[self._size - 1]
        else:
            tail = self._heap_array[-num_peek:]
            if tail_first:
                tail = tail.flip()
            return list(tail)


    def poll(self, poll_off=1, unpack_single=True, tail_first=True):
        """
        If the heap is empty, return None. Otherwise, 
        perform heapsort in place with self._heap_type at the root, 
        remove the last items in the heap and return them.

        Args:
            poll_off (int): The number of values to poll, minimum 1. Defaults to 1.
            unpack_single (bool): If True and num_peek == 1, then return the single value rather than a list. Defaults to True.
            tail_first (bool): If True, returns values in tail-first order, else in sorted order. Defaults to True.
        
        Returns:
            (dtype, list, NoneType): The last item in the sorted heap, a list containing the last items, or None if the heap was empty.
        """

        # Validate inputs.
        if not isinstance(poll_off, int):
            raise TypeError(f"poll_off must be of type int.\n"
                            f"type(poll_off): {type(poll_off)}.")
        if poll_off < 1:
            raise ValueError(f"poll_off must be positive.\n"
                            f"poll_off: {poll_off}.")

        tail = self.peek_tail(poll_off, unpack_single, tail_first) # Note: sorts self._heap_array.
        self._size -= poll_off
        return tail


    def push(self, new_value):
        """
        Inserts new_value into the heap and restores the heap property. 
        
        If the heap is already at capacity, then new_value is compared to either the head (root) or tail 
        depending on self.overflow_off, and if new_value is less extreme in the direction of the head or tail, 
        then that value is removed and new_value is inserted.
        
        Args:
            new_value (dtype): The value to be inserted
        
        Raises:
            ValueError: Raised if self.overflow_off is encountered as something other than 'head' or 'tail'.
        
        Returns:
            dtype, NoneType: If the heap overflowed then the discarded value is returned, else None is returned.
        """

        if self._size < self._capacity:
            # Add new_value to the first available space in the array, sift up, and increment size.
            self._heap_array[self._size] = new_value
            self._size += 1
            self._sift_up(self._size - 1)
            return None
        else:
            # Already at capacity. Discard and return a value.
            if self.overflow_off == 'head':
                # If the root is not more extreme than new_value, do not insert new_value.
                if not self._is_more_extreme(self._heap_array[0], new_value):
                    return new_value
                else:
                    # Pop and return the root, replacing it with new_value and restoring the heap property.
                    return self.replace(new_value)
            elif self.overflow_off == 'tail':
                # Perform heapsort in place with self._heap_type first, 
                # then replace the last item if it is less extreme than new_value.
                tail = self.peek_tail() # Note: sorts self._heap_array.
                # If the tail is at least as extreme as new_value, do not insert new_value.
                if not self._is_more_extreme(new_value, tail):
                    return new_value
                else:
                    # Replace the tail of self._heap_array with the new_value and return the polled tail.
                    self._size -= 1
                    self.push(new_value)
                    return tail
            else:
                raise ValueError(f"overflow_off must be either 'head' or 'tail'.\n"
                                 f"overflow_off: {overflow_off}.")

    @ staticmethod
    def heapify(array, capacity=None, heap_type='min', overflow_off='head', dtype=float, n_ary=2):
        """
        Construct a heap from array. Its capacity is set to the size of the array.
        
        Args:
            array (np.ndarray): The array to be made into a heap.
            capacity (int, NoneType, optional): The capacity of the new array. None is interpreted as the size of array. Defaults to None.
            heap_type (str, optional): The type of heap to be made, either 'min' or 'max'. Defaults to 'min'.
            overflow_off (str, optional): Determines what to discard when values are pushed when the heap is at capacity, either 'head' or 'tail'. Defaults to 'head'.
            dtype (type, optional): The dtype of the heap. Defaults to float.
            n_ary (int, optional): The maximum number of children for each node, or the branching factor of the tree. Defaults to 2.

        Returns:
            N_ary_heap: The heap constructed from array.
        """

        # Validate inputs.
        array = np.array(array, dtype=dtype)
        if capacity is None:
            capacity = array.size
        if not isinstance(capacity, int):
            raise TypeError(f"capacity must be of type int.\n"
                            f"type(capacity): {type(capacity)}.")
        if capacity < 1:
            raise ValueError(f"capacity must be positive.\n"
                            f"capacity: {capacity}.")

        # Make empty heap capable of holding the entire array.
        heap = N_ary_heap(array.size, heap_type, overflow_off, dtype, n_ary)

        # Manually override heap attributes.
        heap._heap_array = array.flatten() # Note: produces a copy of array, not a view.
        heap._size = array.size

        # Heapify the underlying array.
        n_internal_nodes = heap._n_ary**(np.floor(
            np.log(heap._size) / np.log(heap._n_ary))
        ) - 1
        for index in reversed(range(n_internal_nodes)):
            heap._sift_down(index)

        self.change_capacity(new_capacity)

        return heap


    def change_capacity(self, new_capacity):
        """
        Reassign the underlying self._heap_array to an array of the desired size.
        If the new_capacity is less than the current size of the heap, 
        the excess elements are overflow and are discarded.
        
        Args:
            new_capacity (int): The new capacity of the heap.
        
        Raises:
            TypeError: Raised if new_capacity is not of type int.
            ValueError: Raised if new_capacity is not positive.
        """

        # Validate inputs.
        if not isinstance(new_capacity, int):
            raise TypeError(f"new_capacity must be of type int.\n"
                            f"type(new_capacity): {type(new_capacity)}.")
        if new_capacity < 1:
            raise ValueError(f"new_capacity must be positive.\n"
                            f"new_capacity: {new_capacity}.")
        
        if new_capacity >= self._capacity:
            self._heap_array = np.concatenate((self._heap_array, np.full(new_capacity, np.nan, self.dtype)))
        else:
            self._force_overflow(self.size() - new_capacity)
            self._heap_array = self._heap_array[:self.size()]
        self._capacity = new_capacity

'''
  _        _         _              ____                             _      _____           _              _                     
 | |      (_)       | |            |  _ \                           | |    / ____|         | |            | |                    
 | |       _   ___  | |_   ______  | |_) |   __ _   ___    ___    __| |   | (___    _   _  | |__     ___  | |   __ _   ___   ___ 
 | |      | | / __| | __| |______| |  _ <   / _` | / __|  / _ \  / _` |    \___ \  | | | | | '_ \   / __| | |  / _` | / __| / __|
 | |____  | | \__ \ | |_           | |_) | | (_| | \__ \ |  __/ | (_| |    ____) | | |_| | | |_) | | (__  | | | (_| | \__ \ \__ \
 |______| |_| |___/  \__|          |____/   \__,_| |___/  \___|  \__,_|   |_____/   \__,_| |_.__/   \___| |_|  \__,_| |___/ |___/
                                                                                                                                 
                                                                                                                                 
'''

class Infinite_N_ary_heap(N_ary_heap):

    def __init__(self, heap_type='min', overflow_off='head', dtype=float, n_ary=2):

        super().__init__(1, heap_type, overflow_off, dtype, n_ary)
        self._capacity = np.inf
        self._heap_array = []
        self._heap_list = self._heap_array # Aliasing for clarity.


    def _force_overflow(self, num_overflow):
        """Not implemented in Infinite_N_ary_heap."""

        raise NotImplementedError(f"_force_overflow is not implemented in Infinite_N_ary_heap.")
    

    def push(self, new_value):
        """
        Inserts new_value into the heap and restores the heap property. 
        
        Args:
            new_value (dtype): The value to be inserted
        """

        # Add new_value to the first available space in the array, sift up, and increment size.
        self._heap_list.append(new_value)
        self._size += 1
        self._sift_up(self._size - 1)


    def pop(self):
        """
        Gracefully removes and returns the root. If the heap is empty, returns None.
        
        Returns:
            dtype: The root of the heap, or None if the heap is empty.
        """
    
        root = super().pop()

        if root is not None:
            del self._heap_list [-1]
        
        return root

    
    def poll(self, poll_off=1, unpack_single=True, tail_first=True):
        """
        If the heap is empty, return None. Otherwise, 
        perform heapsort in place with self._heap_type at the root, 
        remove the last items in the heap and return them.

        Args:
            poll_off (int): The number of values to poll, minimum 1. Defaults to 1.
            unpack_single (bool): If True and num_peek == 1, then return the single value rather than a list. Defaults to True.
            tail_first (bool): If True, returns values in tail-first order, else in sorted order. Defaults to True.
        
        Returns:
            (dtype, list, NoneType): The last item in the sorted heap, a list containing the last items, or None if the heap was empty.
        """

        tail = super().poll(poll_off, unpack_single, tail_first)
        del self._heap_list[-poll_off:]
        return tail


    def change_capacity(self, new_capacity):
        """
        Not implemented in Infinite_N_ary_heap.
        
        Args:
            new_capacity (int): The new capacity of the heap.
        
        Raises:
            NotImplementedError: This method raises a NotImplementedError in the Infinite_N_ary_heap subclass.
        """

        raise NotImplementedError(f"change_capacity is not implemented in Infinite_N_ary_heap.")