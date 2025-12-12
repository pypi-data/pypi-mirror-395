import torch
import torch.nn as nn
import torch.optim as optim

class PowerPlantNN(nn.Module):
    def __init__(self, input_dim=4, hidden_layers=[64, 32]):
        super(PowerPlantNN, self).__init__()
        layers = []
        in_dim = input_dim
        
        # Dynamically build layers based on the list provided
        for h_dim in hidden_layers:
            layers.append(nn.Linear(in_dim, h_dim))
            layers.append(nn.ReLU()) # Activation function
            in_dim = h_dim
            
        # Final output layer (1 output for Energy Prediction)
        layers.append(nn.Linear(in_dim, 1))
        
        self.network = nn.Sequential(*layers)
        self.criterion = nn.MSELoss() # Neural Nets typically use MSE

    def forward(self, x):
        return self.network(x)
    
    def fit(self, X_train, y_train, epochs=500, lr=0.001):
        if not isinstance(X_train, torch.Tensor):
            X_train = torch.tensor(X_train, dtype=torch.float32)
        if not isinstance(y_train, torch.Tensor):
            y_train = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
            
        optimizer = optim.Adam(self.parameters(), lr=lr)
        self.train()
        
        for epoch in range(epochs):
            optimizer.zero_grad()
            outputs = self(X_train)
            loss = self.criterion(outputs, y_train)
            loss.backward()
            optimizer.step()
            
    def predict(self, X):
        if not isinstance(X, torch.Tensor):
            X = torch.tensor(X, dtype=torch.float32)
        self.eval()
        with torch.no_grad():
            return self(X).numpy()
            
    def get_architecture(self):
        print(self.network)