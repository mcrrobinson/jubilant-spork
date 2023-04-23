from random import randbytes
from shamira import generate, generate_raw, reconstruct, reconstruct_raw

# secret = bytearray(randbytes(8))
secret = "secret"

key = generate(secret, 3, 5)


key.pop()
key.pop()
key.pop()

print(key)

result = reconstruct(*key, encoding='b32')
print(result)
# class Shamir:
    
#     def split(secret: bytearray, parts:int, threshold:int) -> list[bytearray]:
#         if parts < threshold:
#             raise Exception("Parts must be greater than threshold")
#         elif parts > 255:
#             raise Exception("Parts must be less than 256")
#         elif threshold < 2:
#             raise Exception("Threshold must be greater than 1")
#         elif threshold > 255:
#             raise Exception("Threshold must be less than 256")
#         elif len(secret) == 0:
#             raise Exception("Cannot split empty secret")
        