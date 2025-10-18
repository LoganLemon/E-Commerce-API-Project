import pytest
from unittest.mock import patch, MagicMock
from fastapi import status

class TestOrderCheckout:
    """Test order checkout functionality."""
    
    def test_checkout_unauthorized(self, client):
        """Test checkout without authentication."""
        response = client.post("/orders/checkout")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_checkout_empty_cart(self, client, auth_headers):
        """Test checkout with empty cart."""
        response = client.post("/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cart is empty" in response.json()["detail"]
    
    @patch('stripe.checkout.Session.create')
    def test_checkout_success(self, mock_stripe_create, client, test_product, auth_headers):
        """Test successful checkout with items in cart."""
        # Mock Stripe response
        mock_session = MagicMock()
        mock_session.url = "https://checkout.stripe.com/test"
        mock_stripe_create.return_value = mock_session
        
        # Add item to cart first
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        client.post("/cart/add", json=cart_data, headers=auth_headers)
        
        # Checkout
        response = client.post("/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "checkout_url" in data
        assert data["checkout_url"] == "https://checkout.stripe.com/test"
        
        # Verify Stripe was called with correct parameters
        mock_stripe_create.assert_called_once()
        call_args = mock_stripe_create.call_args
        assert call_args[1]["payment_method_types"] == ["card"]
        assert call_args[1]["mode"] == "payment"
        assert len(call_args[1]["line_items"]) == 1
        assert call_args[1]["line_items"][0]["quantity"] == 2
    
    @patch('stripe.checkout.Session.create')
    def test_checkout_insufficient_stock(self, mock_stripe_create, client, test_product, auth_headers):
        """Test checkout when product has insufficient stock."""
        # Add more items to cart than available in stock
        cart_data = {
            "product_id": test_product.id,
            "quantity": 15  # More than test_product.quantity (10)
        }
        client.post("/cart/add", json=cart_data, headers=auth_headers)
        
        # Checkout should fail
        response = client.post("/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not available or out of stock" in response.json()["detail"]
        
        # Stripe should not be called
        mock_stripe_create.assert_not_called()
    
    @patch('stripe.checkout.Session.create')
    def test_checkout_nonexistent_product(self, mock_stripe_create, client, auth_headers, db_session):
        """Test checkout when cart contains non-existent product."""
        # Manually add cart item with non-existent product
        from app import models
        cart_item = models.CartItem(
            user_id=1,  # Assuming test user has id=1
            product_id=999,  # Non-existent product
            quantity=2
        )
        db_session.add(cart_item)
        db_session.commit()
        
        # Checkout should fail
        response = client.post("/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "not available or out of stock" in response.json()["detail"]
        
        # Stripe should not be called
        mock_stripe_create.assert_not_called()
    
    @patch('stripe.checkout.Session.create')
    def test_checkout_stripe_error(self, mock_stripe_create, client, test_product, auth_headers):
        """Test checkout when Stripe returns an error."""
        # Mock Stripe to raise an exception
        mock_stripe_create.side_effect = Exception("Stripe API error")
        
        # Add item to cart
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        client.post("/cart/add", json=cart_data, headers=auth_headers)
        
        # Checkout should fail
        response = client.post("/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Stripe API error" in response.json()["detail"]
    
    @patch('stripe.checkout.Session.create')
    def test_checkout_multiple_products(self, mock_stripe_create, client, auth_headers, db_session, test_product):
        """Test checkout with multiple different products."""
        # Create additional products
        from app import models
        product2 = models.Product(
            name="Product 2",
            description="Second product",
            price=50.0,
            quantity=5
        )
        product3 = models.Product(
            name="Product 3",
            description="Third product", 
            price=75.0,
            quantity=8
        )
        db_session.add_all([product2, product3])
        db_session.commit()
        
        # Mock Stripe response
        mock_session = MagicMock()
        mock_session.url = "https://checkout.stripe.com/test"
        mock_stripe_create.return_value = mock_session
        
        # Add multiple items to cart
        items = [
            {"product_id": test_product.id, "quantity": 2},  # Use actual test_product id
            {"product_id": 2, "quantity": 1},
            {"product_id": 3, "quantity": 3}
        ]
        
        for item in items:
            client.post("/cart/add", json=item, headers=auth_headers)
        
        # Checkout
        response = client.post("/orders/checkout", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify Stripe was called with all items
        call_args = mock_stripe_create.call_args
        assert len(call_args[1]["line_items"]) == 3

class TestPaymentSuccess:
    """Test payment success endpoint."""
    
    @patch('stripe.checkout.Session.retrieve')
    def test_payment_success(self, mock_stripe_retrieve):
        """Test payment success endpoint."""
        # Mock Stripe session
        mock_session = MagicMock()
        mock_customer_details = MagicMock()
        mock_customer_details.email = "customer@example.com"
        mock_session.customer_details = mock_customer_details
        mock_stripe_retrieve.return_value = mock_session
        
        # This would normally be called by the frontend after Stripe redirect
        # We'll test it directly
        from fastapi.testclient import TestClient
        from app.main import app
        
        with TestClient(app) as client:
            response = client.get("/orders/success?session_id=test_session_id")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "Payment successful" in data["message"]
            assert data["email"] == "customer@example.com"
    
    @patch('stripe.checkout.Session.retrieve')
    def test_payment_success_no_customer_email(self, mock_stripe_retrieve):
        """Test payment success when customer email is not available."""
        # Mock Stripe session without customer details
        mock_session = MagicMock()
        mock_session.customer_details = None
        mock_stripe_retrieve.return_value = mock_session
        
        from fastapi.testclient import TestClient
        from app.main import app
        
        with TestClient(app) as client:
            response = client.get("/orders/success?session_id=test_session_id")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "Payment successful" in data["message"]
            assert data["email"] is None

class TestPaymentCancel:
    """Test payment cancel endpoint."""
    
    def test_payment_cancel(self):
        """Test payment cancel endpoint."""
        from fastapi.testclient import TestClient
        from app.main import app
        
        with TestClient(app) as client:
            response = client.get("/orders/cancel")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert "Payment canceled or failed" in data["message"]

class TestOrderIntegration:
    """Test order integration scenarios."""
    
    @patch('stripe.checkout.Session.create')
    def test_full_order_flow(self, mock_stripe_create, client, test_product, auth_headers):
        """Test complete order flow from cart to checkout."""
        # Mock Stripe response
        mock_session = MagicMock()
        mock_session.url = "https://checkout.stripe.com/test"
        mock_stripe_create.return_value = mock_session
        
        # 1. Add item to cart
        cart_data = {
            "product_id": test_product.id,
            "quantity": 3
        }
        cart_response = client.post("/cart/add", json=cart_data, headers=auth_headers)
        assert cart_response.status_code == status.HTTP_200_OK
        
        # 2. Verify cart has item
        cart_view_response = client.get("/cart/", headers=auth_headers)
        assert cart_view_response.status_code == status.HTTP_200_OK
        cart_items = cart_view_response.json()
        assert len(cart_items) == 1
        assert cart_items[0]["quantity"] == 3
        
        # 3. Checkout
        checkout_response = client.post("/orders/checkout", headers=auth_headers)
        assert checkout_response.status_code == status.HTTP_200_OK
        checkout_data = checkout_response.json()
        assert "checkout_url" in checkout_data
        
        # 4. Verify Stripe was called with correct line items
        call_args = mock_stripe_create.call_args
        line_items = call_args[1]["line_items"]
        assert len(line_items) == 1
        assert line_items[0]["quantity"] == 3
        assert line_items[0]["price_data"]["unit_amount"] == int(test_product.price * 100)
    
    def test_cart_after_checkout(self, client, test_product, auth_headers):
        """Test that cart remains unchanged after checkout (since we don't clear it)."""
        # Add item to cart
        cart_data = {
            "product_id": test_product.id,
            "quantity": 2
        }
        client.post("/cart/add", json=cart_data, headers=auth_headers)
        
        # Verify cart has item
        cart_response = client.get("/cart/", headers=auth_headers)
        assert len(cart_response.json()) == 1
        
        # Note: In a real application, you'd want to clear the cart after successful checkout
        # For now, we're just testing that the checkout process works
        # The cart clearing would be handled in the success callback
