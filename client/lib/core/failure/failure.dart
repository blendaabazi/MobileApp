class AppFailure{
    final String message;
    AppFailure([this.message = 'Sorry, an unexpected error ocurred!']);

    @override
    String toString() => 'AppFailure(message: $message)';
}