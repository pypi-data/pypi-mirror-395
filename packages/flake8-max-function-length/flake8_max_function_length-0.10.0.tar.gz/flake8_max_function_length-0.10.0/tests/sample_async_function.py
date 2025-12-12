async def function(
    first_argument: int,
    second_argument: int,
    third_argument: int,
    fourth_argument: int,
    fifth_argument: int,
    sixth_argument: int,
):
    """some docstring"""

    first_argument += 1

    second_argument += 1

    third_argument += 1
    # comment
    fourth_argument += 1
    fifth_argument += 1
    sixth_argument += 1

    return (
        first_argument,
        second_argument,
        # another comment
        third_argument,
        fourth_argument,
        fifth_argument,
        sixth_argument,
    )
