#### Class
class Essentials():

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