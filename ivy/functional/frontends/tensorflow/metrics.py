import ivy


def binary_matches(y_true, y_pred, threshold=0.5):
    y_pred = ivy.array(y_pred)
    threshold = ivy.astype(ivy.array(threshold), y_pred.dtype)
    y_pred = ivy.astype(ivy.greater(y_pred, threshold), y_pred.dtype)
    return ivy.astype(
        ivy.equal(y_true, y_pred), ivy.default_float_dtype(as_native=True)
    )


def binary_accuracy(y_true, y_pred, threshold=0.5):
    return ivy.mean(binary_matches(y_true, y_pred, threshold), axis=-1)


def sparse_categorical_crossentropy(y_true, y_pred, from_logits=False, axis=-1):
    if from_logits:
        y_pred = ivy.softmax(y_pred)
    return ivy.sparse_cross_entropy(y_true, y_pred, axis=axis)


def binary_crossentropy(y_true, y_pred,
                        from_logits: bool = False,
                        label_smoothing: float = 0.) -> ivy.Array:
    """Computes the binary crossentropy loss.
    Parameters
    ----------
        y_true:
            Ground truth values.
        y_pred:
            The predicted values.
        from_logits: bool
            Whether `y_pred` is expected to be a logits array/tensor. By default,
            we assume that `y_pred` encodes a probability distribution.
        label_smoothing: Float
            in [0, 1]. If > `0` then smooth the labels by
            squeezing them towards 0.5 That is, using `1. - 0.5 * label_smoothing`
            for the target class and `0.5 * label_smoothing` for the non-target class.
    Returns
    -------
        Binary crossentropy loss value.
    """

    if from_logits:
        y_pred = ivy.softmax(y_pred)
    return ivy.mean(ivy.binary_cross_entropy(y_true,
                                             y_pred, label_smoothing))


sparse_categorical_crossentropy.unsupported_dtypes = {"torch": ("float16", "bfloat16")}
