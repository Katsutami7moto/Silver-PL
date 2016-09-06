
# def mysqrt(n):
#     def s(a):
#         if a * a - n > 0.000000001:
#             return s(0.5 * (a + n / a))
#         else:
#             return a
#
#     return s(n)
#
#
# print(mysqrt(123456))

# =>


# class mysqrt__closured:
#     def __init__(self, n):
#         self.n = n
#
#     def mysqrt(self):
#         return self.s(self.n)
#
#     def s(self, a):
#         if a * a - self.n > 0.000000001:
#             return self.s(0.5 * (a + self.n / a))
#         else:
#             return a
#
# print(mysqrt__closured(123456).mysqrt())
