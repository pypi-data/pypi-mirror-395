"""
快速排序
"""

def _partition(A:list[int],p:int,q:int) -> int:
  """
  对数组原地排序
  参数：
    A (n,) : 长度为n的数组
    p int  : 左指针
    q int  : 右指针
  返回值：
    i      : 返回值是pivot的位置
  """
  x = A[p] # pivot
  i = p
  for j in range(p+1,q):
    if A[j] <= x:
      i += 1
      A[i], A[j] = A[j] , A[i]
  A[p], A[i] = A[i], A[p]
  return i

def _quick_sort(A:list[int],p:int,r:int) -> None:
  """
  快速排序，递归调用
  参数：
    A (n,) : 长度为n的数组
    p int  : 左指针
    r int  : 右指针
  返回值：
    None
  """
  if p < r:
    q = _partition(A,p,r)
    _quick_sort(A,p,q)
    _quick_sort(A,q+1,r)
  return A

def quick_sort(A):
  n = len(A)
  return _quick_sort(A,0,n)

def example_quick_sort():
  """
  案例展示
  """
  A = [6,10,13,5,8,3,2,11]
  n = len(A)
  _quick_sort(A,0,n)
  print(A)


"""
计数排序
"""

def counting_sort(a):
  k = max(a) - min(a)
  n = len(a)
  b = [0] * n
  c = [_ for _ in range(k+1)]
  for i in a:
    c[i] += 1
  for i in range(k):
    c[i] += c[i-1]
  for j in range(n,0,-1):
    b[c[a[j]]] = a[j]
    c[j] -= 1
  return b
def test_couting_sort():
  a = [4,1,3,4,3,0]
  print(counting_sort(a))
# test_couting_sort()

'''
基数排序
'''

def redix_sort(a):
  pass
