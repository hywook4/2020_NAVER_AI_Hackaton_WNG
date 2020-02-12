def get_intersection_area(r1, r2):
    x1, y1, x2, y2 = r1
    a1, b1, a2, b2 = r2

    bottom = max(x1, a1)
    top = min(x2, a2)
    left = max(y1, b1)
    right = min(y2, b2)

    if left <= right and bottom <= top:
        return (right-left)*(top-bottom)
    
    return 0
