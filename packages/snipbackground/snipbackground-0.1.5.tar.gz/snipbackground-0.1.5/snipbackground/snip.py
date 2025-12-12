import numpy as np

def snip_background(x, y_val, m=30):
    """
    Fast, vectorized CPU implementation of the SNIP background algorithm.
    """

    # Accept 1D input by converting to 2D
    if y_val.ndim == 1:
        y_val = y_val.reshape(1, -1)

    n_spectra, N = y_val.shape

    SNIPed_spectra = np.zeros_like(y_val)
    b_spectra = np.zeros_like(y_val)

    for i in range(n_spectra):
        y = y_val[i].astype(float)

        # Step 1: Logarithmic pre-scaling
        v = np.log(np.log(np.sqrt(y + 1) + 1) + 1)

        # Step 2: SNIP smoothing
        for p in range(1, m + 1):
            left  = np.roll(v, p)
            right = np.roll(v, -p)
            avg_lr = 0.5 * (left + right)
            v[p:N-p] = np.minimum(v[p:N-p], avg_lr[p:N-p])

        # Step 3: Reverse transform
        b = (np.exp(np.exp(v) - 1) - 1)**2 - 1

        # Step 4: Background subtraction
        SNIPed = y - b
        low_limit = abs(np.mean(SNIPed) * 0.1)
        SNIPed = np.clip(SNIPed, low_limit, None)

        SNIPed_spectra[i] = SNIPed
        b_spectra[i] = b

    return SNIPed_spectra, b_spectra