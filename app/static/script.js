let isLoggedIn = false;

function showToast(message = "", type = "info", duration = 3000) {
    const toast = document.getElementById("toast");
    const icon = document.getElementById("toast-icon");
    const msg = document.getElementById("toast-message");

    let iconSymbol = "ℹ️";

    switch (type) {
        case "success":
            iconSymbol = "✅";
            break;
        case "error":
            iconSymbol = "❌";
            break;
        case "warn":
            iconSymbol = "⚠️";
            break;
        default:
            iconSymbol = "ℹ️";
    }

    icon.textContent = iconSymbol;
    msg.textContent = message;

    toast.classList.remove("hidden");
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
        toast.classList.add("hidden");
    }, duration);
}
function showSpinner() {
    document.getElementById("spinner").classList.remove("hidden");
}

function hideSpinner() {
    document.getElementById("spinner").classList.add("hidden");
}


async function register() {
    const username = document.getElementById("reg-username").value.trim();
    const fullName = document.getElementById("reg-fullname").value.trim();
    const password = document.getElementById("reg-password").value.trim();

    if (!username || !fullName || !password) {
        showToast("Please fill in all registration fields.", "warn");
        return;
    }

    const params = new URLSearchParams();
    params.append("username", username);
    params.append("full_name", fullName);
    params.append("password", password);

    const res = await fetch("/register", {
        method: "POST",
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: params
    });

    const data = await res.json();

    if (res.ok) {
        showToast("User created successfully!", "success");
    } else {
        showToast(data.detail || "Registration failed", "error");
    }
}


async function login() {
    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value.trim();

    if (!username || !password) {
        showToast("Please fill in both username and password.", "warn");
        return;
    }
    showSpinner();
    try {
        const params = new URLSearchParams();
        params.append("username", username);
        params.append("password", password);

        const res = await fetch("/login", {
            method: "POST",
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: params
        });

        if (res.ok) {
            isLoggedIn = true;

            document.getElementById("auth").style.display = "none";
            document.getElementById("dashboard").style.display = "block";
            document.getElementById("transaction-page").style.display = "none";

            document.getElementById("current-user").innerText = username;
            // document.getElementById("avatar").setAttribute("data-jdenticon-value", username);
            // jdenticon.update();

            await loadBalance();
            await loadTransactions();
            await loadNetworkTransactions();
            showToast("Logged in successfully!", "success");

        } else {
            alert(await res.text());
            showToast("Login failed!", "error");
        }
    } finally {
        hideSpinner();
    }

// Refresh transactions every 10 seconds
setInterval(() => {
  if (isLoggedIn) {
    loadTransactions();
    loadNetworkTransactions();
  }
}, 10000);

}

async function logout() {
    await fetch("/logout", {method: "POST"});
    isLoggedIn = false;
    // Show login/register
    document.getElementById("auth").style.display = "block";
    showToast("Logged out successfully!", "success")

    // Hide dashboard and transaction page
    document.getElementById("dashboard").style.display = "none";
    document.getElementById("transaction-page").style.display = "none";
}


async function loadBalance() {
    const res = await fetch("/balance/");
    if (res.ok) {
        const data = await res.json();
        document.getElementById("balance").innerText = data.balance;
    } else {
        document.getElementById("balance").innerText = "N/A";
    }
}


async function sendTransaction() {
    const sender = document.getElementById("current-user").innerText.trim();
    const receiver = document.getElementById("to-user").value.trim();
    const amountValue = document.getElementById("amount").value.trim();

    // Validate all fields
    if (!receiver || !amountValue) {
        showToast("Please fill in both recipient and amount.", "warn");
        return;
    }

    const amount = parseFloat(amountValue);
    if (isNaN(amount) || amount <= 0) {
        showToast("Please enter a valid amount greater than 0.", "warn");
        return;
    }

    const payload = {
        sender: sender,
        receiver: receiver,
        amount: amount
    };

    showSpinner();

    try {
        const res = await fetch("/transaction/", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await res.text();

        if (res.ok) {
            showToast(result, "success");
            await loadBalance();
            await loadTransactions();
        } else {
            showToast(result || "Transaction failed", "error");
        }
    } catch (error) {
        console.error("Transaction error:", error);
        showToast("Something went wrong while sending.", "error");
    } finally {
        hideSpinner();
    }
}


async function loadTransactions() {
  const res = await fetch("/transactions/");
  const data = await res.json();
  const div = document.getElementById("transactions");
  const time = document.getElementById("last-updated");

  if (!data.transactions || data.transactions.length === 0) {
    div.innerHTML = "<p>No personal transactions yet.</p>";
    time.innerText = "Last updated: just now";
    return;
  }

  div.innerHTML = "";
  data.transactions.forEach(tx => {
    div.innerHTML += `
      <p>
        <span><strong>🟢 ${tx.sender}</strong> → <strong>🔵 ${tx.receiver}</strong></span>
        <span>💸 ${tx.amount} <small>@ ${tx.timestamp}</small></span>
      </p>`;
  });

  const now = new Date();
  time.innerText = `Last updated: ${now.toLocaleTimeString()}`;
}


async function loadNetworkTransactions() {
    const div = document.getElementById("network-transactions");

    const res = await fetch("/transactions_network/");

    if (!res.ok) {
        const text = await res.text();
        console.error("Network transactions fetch error:", text);
        div.innerHTML = "<p>Error loading network transactions.</p>";
        showToast("Network fetch failed.", "error");
        return;
    }

    const data = await res.json();
    console.log("Network transactions loaded:", data);

    if (data.transactions.length === 0) {
        div.innerHTML = "<p>No transactions yet.</p>";
        return;
    }

    div.innerHTML = "";
    div.classList.add("network-transactions");
data.transactions.forEach(tx => {
    div.innerHTML += `
        <p>
            <span><strong>${tx.sender}</strong> → <strong>${tx.receiver}</strong></span>
            <span>💸 ${tx.amount} <small>@ ${tx.timestamp}</small></span>
        </p>`;
});

}


function showDashboard() {
    if (!isLoggedIn) {
        showToast("Please login first", "warn");
        document.getElementById("auth").style.display = "block";
        document.getElementById("dashboard").style.display = "none";
        document.getElementById("transaction-page").style.display = "none";
        return;

    }

    document.getElementById("auth").style.display = "none";
    document.getElementById("dashboard").style.display = "block";
    document.getElementById("transaction-page").style.display = "none";
}

function showTransactionPage() {
    if (!isLoggedIn) {
        showToast("Please login first", "warn");
        document.getElementById("auth").style.display = "block";
        document.getElementById("dashboard").style.display = "none";
        document.getElementById("transaction-page").style.display = "none";
        return;
    }

    document.getElementById("auth").style.display = "none";
    document.getElementById("dashboard").style.display = "none";
    document.getElementById("transaction-page").style.display = "block";
}


// async function loadNetworkBalance() {
//     const res: await fetch("/balance_Network/");
//
// }
