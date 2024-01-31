const log = (msg) => {
    let notif = document.getElementById("notifications");
    notif.innerHTML = msg;
}

const add_token = (token) => {
    window.pywebview.api.add_account(token).then((callback) => {
        if (callback) {
            load_accounts();
            log(`added account: ${callback.username}`)
        } else {
            log('failed to add the account')
        }
    });
}

const paste_token = () => {
    let popout = document.getElementById("popout");
    
    popout.style.display = "flex";

    submit = document.getElementById("submit");

    submit.addEventListener("click", () => {
        let token = document.getElementById("token").value;
        add_token(token);
        popout.style.display = "none";
    });
}

const add_account = () => {
    window.pywebview.api.get_account_token().then((token) => {
        if (token) {
            add_token(token);
            
        } else {
            log('failed to add the account')
        }
    });
}

const remove_account = (id) => {
    window.pywebview.api.remove_account(id).then((callback) => {
        if (callback) {
            load_accounts();
            log(`removed account ${callback.username}`)
        } else {
            log('failed to remove the account')
        }
    });
}

const copy_token_from_user_id = (id) => {
    window.pywebview.api.trade_id_for_token(id).then((token) => {
        if (token) {
            navigator.clipboard.writeText(token);
            log('copied token')
        }
    });
}

const login = (id) => {
    window.pywebview.api.login(id).then((callback) => {
        if (callback) {
            log(`logged in as ${callback.username}`)
        } else {
            log('failed to login')
        }
    });
}

const load_accounts = () => {
    window.pywebview.api.get_accounts().then((accounts) => {
        console.log(accounts);

        let accountList = document.getElementById("accounts");
        accountList.innerHTML = "";

        for (let i = 0; i < accounts.length; i++) {
            let acc = accounts[i];
            let accUser = document.createElement("div");
            accUser.classList.add("account");
            accUser.innerHTML = `
       
                <div class="account__user">
                    <img class="account__user__img" src="https://cdn.discordapp.com/avatars/${acc.id}/${acc.avatar}"></img>
                    <div class="account__user__info">
                        <span class="account__user__display">${acc.display_name}</span>
                        <span class="account__user__name">@${acc.username}</span>
                        <span class="account__user__id">${acc.id}</span>
                    </div>
                </div>

                <div class="account__controls">
                    <button class="account__controls__login" onclick="login('${acc.id}')">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="currentColor" d="M352 96l64 0c17.7 0 32 14.3 32 32l0 256c0 17.7-14.3 32-32 32l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l64 0c53 0 96-43 96-96l0-256c0-53-43-96-96-96l-64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32zm-9.4 182.6c12.5-12.5 12.5-32.8 0-45.3l-128-128c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L242.7 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l210.7 0-73.4 73.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l128-128z"/></svg>
                    </button>
                    <button class="account__controls__copy" onclick="copy_token_from_user_id('${acc.id}');">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"/></svg>
                    </button>
                    <button class="account__controls__delete" onclick="remove_account('${acc.id}')">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg>
                    </button>
                </div>
            `;
            accountList.appendChild(accUser);
        }
    });
}

window.addEventListener('pywebviewready', function() {

    document.getElementById("close").addEventListener("click", () => {window.pywebview.api.close()});
    document.getElementById("minimize").addEventListener("click", () => {window.pywebview.api.minimize()});

    document.getElementById("addtoken").addEventListener("click", paste_token);
    document.getElementById("addaccount").addEventListener("click", add_account);
    document.getElementById("popout").addEventListener("click", (e) => {
            if (e.target.id == "popout") {
                document.getElementById("popout").style.display = "none";
            }
        }
    );

    document.getElementById('accounts').addEventListener('mouseenter', function(e){
        e.target.style.overflow = 'auto';
    }, false);

    document.getElementById('accounts').addEventListener('mouseleave', function(e){
        e.target.style.overflow = 'hidden';
    }, false);

    load_accounts();
});
