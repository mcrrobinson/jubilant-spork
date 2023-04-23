class Shamir:

    @staticmethod
    def interpolate_polynomial(x: int, x_samples: list, y_samples: list) -> int:
        if len(x_samples) != len(y_samples):
            print("x_samples and y_samples must be the same length")
            return

        if len(x_samples) < 2:
            print("Not enough samples to interpolate.")
            return

        y = 0

        for i in range(len(x_samples)):
            numerator = 1
            denominator = 1
            for j in range(len(x_samples)):
                if i == j:
                    continue

                numerator *= x - x_samples[j]
                denominator *= x_samples[i] - x_samples[j]

            y += y_samples[i] * numerator / denominator

        return y

    @staticmethod
    def combine(parts: list):
        if len(parts) < 2:
            print("Not enough parts to combine.")
            return

        firstPartLen = len(parts[0])
        if firstPartLen < 2:
            print("Parts must be at least two bytes")

        for i in range(1, len(parts)):
            if len(parts[i]) != firstPartLen:
                print("Parts must be the same length")
                return

        secret = bytearray(firstPartLen - 1)

        x_samples = [0 * len(parts)]
        y_samples = [0 * len(parts)]

        # byte to bool map
        check_map = {}

        for i in range(parts):
            part = parts[i]
            samp = part[firstPartLen - 1]
            if exists := check_map.get(samp):
                if exists:
                    print("Duplicate sample")
                    return

            check_map[samp] = True
            x_samples[i] = samp

        for idx in range(secret):
            for i in range(len(parts)):
                y_samples[i] = parts[i][idx]

            secret[idx] = Shamir.interpolate_polynomial(
                0, x_samples, y_samples)

        return secret
