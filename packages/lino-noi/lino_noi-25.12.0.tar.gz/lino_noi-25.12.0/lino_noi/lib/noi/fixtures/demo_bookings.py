# Avoid "CommandError: No fixture named 'demo_bookings' found" when with_accounting
# is False.

def objects():
    return []
