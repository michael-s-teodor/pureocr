#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Mihnea S. Teodorescu & Moe Assaf, University of Groningen
"""

#### Class declaration
class Essentials():
    # Sorting algorithms
    def wham_sort(length, arr):
        # Break recursive step
        if (length <= 1):
            return
        
        prefix = [None] * length
        suffix = [None] * length
        
        # Get prefix length
        p = 1
        while (p < length):
            if (arr[p-1] > arr[p]):
                break
            p += 1

        while (length - p):
            # Get prefix
            prefix[0] = arr[0]
            p = 1
            while (p < length):
                if (arr[p-1] <= arr[p]):
                    prefix[p] = arr[p]
                else:
                    break
                p += 1
            
            # Get suffix
            s = 0
            while (s < p):
                if (p+s >= length):
                    break
                suffix[s] = arr[p+s]
                s += 1

            # Next recursive step
            wham_sort(s, suffix)

            # Merge prefix and (now sorted) suffix into arr
            l     =  p
            r     =  s
            p     += s
            idx   =  0
            left  =  0
            right =  0
            while (left < l and right < r):
                if (prefix[left] < suffix[right]):
                    arr[idx] = prefix[left]
                    left += 1
                else:
                    arr[idx] = suffix[right]
                    right += 1
                idx += 1
            if (left >= l):
                while (right < r):
                    arr[idx] = suffix[right]
                    idx += 1
                    right += 1
            else:
                while (left < l):
                    arr[idx] = prefix[left]
                    idx += 1
                    left += 1
    
    def wham_sort_by(self, length, arr, by):
        # Break recursive step
        if (length <= 1):
            return
        
        prefix = [None] * length
        suffix = [None] * length
        
        # Get prefix length
        p = 1
        while (p < length):
            if (arr[p-1][by] > arr[p][by]):
                break
            p += 1

        while (length - p):
            # Get prefix
            prefix[0] = arr[0]
            p = 1
            while (p < length):
                if (arr[p-1][by] <= arr[p][by]):
                    prefix[p] = arr[p]
                else:
                    break
                p += 1
            
            # Get suffix
            s = 0
            while (s < p):
                if (p+s >= length):
                    break
                suffix[s] = arr[p+s]
                s += 1

            # Next recursive step
            self.wham_sort_by(s, suffix, by) 

            # Merge prefix and (now sorted) suffix into arr
            l     =  p
            r     =  s
            p     += s
            idx   =  0
            left  =  0
            right =  0
            while (left < l and right < r):
                if (prefix[left][by] < suffix[right][by]):
                    arr[idx] = prefix[left]
                    left += 1
                else:
                    arr[idx] = suffix[right]
                    right += 1
                idx += 1
            if (left >= l):
                while (right < r):
                    arr[idx] = suffix[right]
                    idx += 1
                    right += 1
            else:
                while (left < l):
                    arr[idx] = prefix[left]
                    idx += 1
                    left += 1
    
    def bubble_sort(arr):
        length = len(arr)
        for i in range(length-1):
            for j in range(length-1):
                if (arr[j] > arr[j+1]):
                    temp = arr[j+1]
                    arr[j+1] = arr[j]
                    arr[j] = temp
        return arr
    
    def bubble_sort_by(arr, by):
        length = len(arr)
        for i in range(length-1):
            for j in range(length-1):
                if (arr[j][by] > arr[j+1][by]):
                    temp = arr[j+1]
                    arr[j+1] = arr[j]
                    arr[j] = temp
        return arr
    
    # Searching algorithms
    def binary_search(length, arr, value):
        left = 0
        right = length
        mid
        while (left + 1 < right):
            mid = (left + right)/2
            if (value < arr[mid]):
                right = mid
            else:
                left = mid
        if (length == 0 or arr[left] != value):
            return -1
        else:
            return left

