"""
Library Analytics Core Module

This module provides analytics functionality for library management systems.
It can work with Django ORM or any database that provides similar query interfaces.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class LibraryAnalytics:
    """
    Main analytics class for library management systems.

    This class provides methods to generate various analytics reports
    including inventory summaries, checkout reports, and popular books analysis.
    """

    def __init__(self, book_model=None, transaction_model=None, timezone_module=None):
        """
        Initialize the analytics service.

        Args:
            book_model: The Book/BookLog model class (Django model or similar)
            transaction_model: The Transaction model class
            timezone_module: Timezone utility module (e.g., django.utils.timezone)
        """
        self.book_model = book_model
        self.transaction_model = transaction_model
        self.timezone = timezone_module

        # Try to auto-import Django models if not provided
        if book_model is None or transaction_model is None:
            try:
                from books.models import BookLog, Transaction
                self.book_model = book_model or BookLog
                self.transaction_model = transaction_model or Transaction
            except ImportError:
                pass

        # Try to auto-import Django timezone if not provided
        if timezone_module is None:
            try:
                from django.utils import timezone as tz
                self.timezone = tz
            except ImportError:
                pass

    def inventory_summary(self) -> Dict[str, int]:
        """
        Generate inventory summary statistics.

        Returns:
            Dictionary containing:
            - total_books: Total number of unique books
            - stock_in: Number of books currently available
            - stock_out: Number of books currently out of stock
            - total_copies: Total number of book copies
        """
        if not self.book_model:
            raise ValueError("Book model not configured")

        total_books = self.book_model.objects.count()
        stock_in = self.book_model.objects.filter(number_of_books_available__gt=0).count()
        stock_out = self.book_model.objects.filter(number_of_books_available=0).count()

        # Calculate total copies
        total_copies = sum(
            book.number_of_books_available
            for book in self.book_model.objects.all()
        )

        return {
            'total_books': total_books,
            'stock_in': stock_in,
            'stock_out': stock_out,
            'total_copies': total_copies
        }

    def weekly_checkout_report(self, days: int = 7) -> int:
        """
        Get the number of checkouts in the last N days.

        Args:
            days: Number of days to look back (default: 7)

        Returns:
            Number of checkouts in the specified period
        """
        if not self.transaction_model or not self.timezone:
            raise ValueError("Transaction model or timezone not configured")

        start_date = self.timezone.now() - timedelta(days=days)
        return self.transaction_model.objects.filter(
            date_of_checkout__gte=start_date
        ).count()

    def popular_books(self, limit: int = 10) -> List[Any]:
        """
        Get the most popular (most checked out) books.

        Args:
            limit: Maximum number of books to return (default: 10)

        Returns:
            List of books ordered by checkout count (descending)
        """
        if not self.book_model:
            raise ValueError("Book model not configured")

        try:
            from django.db.models import Count

            return list(
                self.book_model.objects.annotate(
                    checkout_count=Count('transactions')
                ).order_by('-checkout_count')[:limit]
            )
        except ImportError:
            # Fallback without Django
            books = self.book_model.objects.all()
            return sorted(
                books,
                key=lambda b: getattr(b, 'checkout_count', 0),
                reverse=True
            )[:limit]

    def least_borrowed_books(self, limit: int = 10) -> List[Any]:
        """
        Get the least borrowed books.

        Args:
            limit: Maximum number of books to return (default: 10)

        Returns:
            List of books ordered by checkout count (ascending)
        """
        if not self.book_model:
            raise ValueError("Book model not configured")

        try:
            from django.db.models import Count

            return list(
                self.book_model.objects.annotate(
                    checkout_count=Count('transactions')
                ).order_by('checkout_count')[:limit]
            )
        except ImportError:
            # Fallback without Django
            books = self.book_model.objects.all()
            return sorted(
                books,
                key=lambda b: getattr(b, 'checkout_count', 0)
            )[:limit]

    def overdue_books(self) -> List[Any]:
        """
        Get all overdue book transactions.

        Returns:
            List of transactions where the book is overdue
        """
        if not self.transaction_model or not self.timezone:
            raise ValueError("Transaction model or timezone not configured")

        today = self.timezone.now().date()
        return list(
            self.transaction_model.objects.filter(
                is_returned=False,
                expected_return_date__lt=today
            ).select_related('book', 'user')
        )

    def genre_distribution(self) -> Dict[str, int]:
        """
        Get the distribution of books by genre.

        Returns:
            Dictionary mapping genre names to book counts
        """
        if not self.book_model:
            raise ValueError("Book model not configured")

        try:
            from django.db.models import Count

            genre_counts = self.book_model.objects.values('genre').annotate(
                count=Count('book_id')
            )

            return {item['genre']: item['count'] for item in genre_counts}
        except ImportError:
            # Fallback without Django
            genres = {}
            for book in self.book_model.objects.all():
                genre = getattr(book, 'genre', 'Unknown')
                genres[genre] = genres.get(genre, 0) + 1
            return genres

    def user_activity(self, user_id: int) -> Dict[str, Any]:
        """
        Get activity statistics for a specific user.

        Args:
            user_id: The user's ID

        Returns:
            Dictionary containing user activity stats
        """
        if not self.transaction_model:
            raise ValueError("Transaction model not configured")

        user_transactions = self.transaction_model.objects.filter(user_id=user_id)

        total_checkouts = user_transactions.count()
        active_checkouts = user_transactions.filter(is_returned=False).count()
        returned_books = user_transactions.filter(is_returned=True).count()

        return {
            'total_checkouts': total_checkouts,
            'active_checkouts': active_checkouts,
            'returned_books': returned_books
        }
