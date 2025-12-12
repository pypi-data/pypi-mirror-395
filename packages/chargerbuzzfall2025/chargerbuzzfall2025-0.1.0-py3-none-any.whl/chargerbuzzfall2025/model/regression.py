import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class CauchyRegression(nn.Module):
    def __init__(self, input_dim=4, c=1.0):
        super(CauchyRegression, self).__init__()
        # Linear layer: y = w0 + w1*x1 + w2*x2 + w3*x3 + w4*x4
        # Note: nn.Linear adds the bias (w0) automatically
        self.linear = nn.Linear(input_dim, 1)
        self.c = c  # The scale parameter for Cauchy loss
        
    def forward(self, x):
        return self.linear(x)
    
    def cauchy_loss(self, y_pred, y_true):
        """
        L(y_hat, y) = (c^2 / 2) * log(1 + ((y - y_hat) / c)^2)
        """
        diff = y_true - y_pred
        loss = (self.c**2 / 2) * torch.log(1 + (diff / self.c)**2)
        return torch.mean(loss)

    def fit(self, X_train, y_train, epochs=1000, lr=0.01):
        """
        Train the model using PyTorch Gradient Descent.
        """
        # Convert numpy arrays to tensors if needed
        if not isinstance(X_train, torch.Tensor):
            X_train = torch.tensor(X_train, dtype=torch.float32)
        if not isinstance(y_train, torch.Tensor):
            y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)

        optimizer = optim.Adam(self.parameters(), lr=lr)
        loss_history = []
        
        self.train()
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self(X_train)
            loss = self.cauchy_loss(outputs, y_train)
            loss.backward()
            optimizer.step()
            loss_history.append(loss.item())
                
        return loss_history

    def predict(self, X):
        """Make predictions."""
        if not isinstance(X, torch.Tensor):
            X = torch.tensor(X, dtype=torch.float32)
        self.eval()
        with torch.no_grad():
            predictions = self(X)
        return predictions.numpy()

    def plot_correlations(self, dataframe):
        """
        Scatterplot matrix showing correlation among features and target.
        """
        plt.figure(figsize=(10, 8))
        sns.pairplot(dataframe, diag_kind='kde')
        plt.suptitle("Feature Correlation Matrix", y=1.02)
        plt.show()

    def save_to_onnx(self, filepath="cauchy_model.onnx"):
        """Save the trained model to ONNX format."""
        self.eval()
        # Create a dummy input matching input_dim (batch_size=1, inputs=4)
        dummy_input = torch.randn(1, self.linear.in_features)
        
        torch.onnx.export(
            self,
            dummy_input,
            filepath,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
        )
        print(f"Model saved to {filepath}")
