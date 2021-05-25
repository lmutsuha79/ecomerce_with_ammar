
let confirm_but = document.getElementById('confirm');

let username = document.querySelector('input[name="username"]');
let valid_username = document.querySelector('.valid_user');
let valid_username_value = true;
username.onkeyup = () => {
    let user_value = username.value;
    if (user_value !== '') {

        if (username.value.toString().length < 2) {
            valid_message_style(valid_username, 0, 'username must be more than 2 characters');
        }
        else {
            check_filed(user_value)
            // if not validate user
        }
    }
    else {
        // remove error when delete every thing

        valid_message_style(valid_username, 1);

    }

};



function valid_message_style(input, true_or_false, text) {
    if (true_or_false === 1) {
        input.classList.remove("valid_message_false");
        input.classList.add("valid_message_true");
        confirm_but.disabled = false;

    }
    else {
        if (text) { input.innerText = text }
        input.classList.remove("valid_message_true");
        input.classList.add("valid_message_false");
        confirm_but.disabled = true;

    }
}

let email_inp = document.querySelector('input[name="email"]');
let valid_mail_message = document.querySelector(".valid_email");
email_inp.onkeyup = () => {
    let email_value = email_inp.value;
    if (email_value !== '') {


        if (ValidateEmail(email_value)) {
            // true valid mail


            valid_message_style(valid_mail_message, 1);

        }
        else {
            // if not validate mail

            valid_message_style(valid_mail_message, 0);

        }
    }
    else {
        // remove error when delete every thing

        valid_message_style(valid_mail_message, 1);

    }

};

// validate of password
let password_inp = document.querySelector('input[name="password"]');
let valid_pass = document.querySelector('.valid_pass');
password_inp.onkeyup = () => {
    let password_inp_value = password_inp.value;

    if (password_inp_value !== '') {
        if (password_inp_value.toString().length < 6) {
            valid_message_style(valid_pass, 0);

        } else {
            valid_message_style(valid_pass, 1);

        }
    }
    else {
        // remove error when delete every thing
        valid_message_style(valid_pass, 1);

    }
}

// confirm password  validation:
let confirm_password_inp = document.querySelector('input[name="confirm"]');
let valid_confirm_pass = document.querySelector('.valid_confirm');

confirm_password_inp.onkeyup = () => {
    let password_inp_value = password_inp.value;
    let confirm_password_inp_value = confirm_password_inp.value;

    if (confirm_password_inp_value === password_inp_value) {
        valid_message_style(valid_confirm_pass, 1);

    } else {
        valid_message_style(valid_confirm_pass, 0);
    }
}

// final check for form
function valid_form() {
    if (username.value.toString().length < 2) {
        valid_message_style(valid_username, 0, 'username must more 2');
        return false
    }
    else if (!valid_username_value) {
        valid_message_style(valid_username, 0, 'user exist');
        return false
    }
    else if (!ValidateEmail(email_inp.value)) {
        valid_message_style(valid_mail_message, 0);
        return false
    }
    else if (password_inp.value.toString().length < 6) {
        valid_message_style(valid_pass, 0);
        return false
    }
    else if (confirm_password_inp.value !== password_inp.value) {
        valid_message_style(valid_confirm_pass, 0);
        return false
    }
    else {
        console.log('tam')

    }

}

// check Username
function check_filed(value) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {

            let result = JSON.parse(this.responseText).result

            if (!result) {
                valid_message_style(valid_username, 0, 'this user exist ');
                valid_username_value = false

            }
            else {
                valid_message_style(valid_username, 1);
                valid_username_value = true
            }
        }
        else {
            valid_message_style(valid_username, 1);
            valid_username_value = true
        }
    };
    xhttp.open("POST", "/check-reg", true);
    xhttp.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xhttp.send("username=" + value);
}


// mail validation:
function ValidateEmail(mail) {
    return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(mail);

}
