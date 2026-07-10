import streamlit as st 
from api import (token_is_valid,register,login,get_current_user,deposit,withdraw,balance,transaction,benefits)
from logger import logger


st.set_page_config(
    page_title="BANK-MANAGEMENT-SYSTEM",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title('Bank Managemnet System🏦')


if 'token' not in st.session_state and 'token' in st.query_params:
    restored_token = st.query_params['token']
    if token_is_valid(restored_token):
        st.session_state['token'] = restored_token
    else:
        st.query_params.clear()

if 'token' not in st.session_state:
    
    st.sidebar.title('Navigation')

    menu = st.sidebar.radio('select an option: ', ['Register','Login'])
    if menu == 'Register':
        st.header('REGISTER')
        with st.form('register_form'):
            username = st.text_input('username')
            password = st.text_input('password',type='password')
            account_type =st.selectbox("Account Type",['savings','current'])
            submit = st.form_submit_button('Register')
            if submit:
                data = {
                    'username':username,
                    'password':password,
                    'account_type':account_type
                }
                response = register(data)
                if response.status_code==201:
                    logger.info(f"user registered :{username}")
                    st.success(f'Dear {username} you have been registered successfully')
                    st.balloons()

                else:
                    logger.warning(f"registration failed :{username}")
                    detail = response.json()["detail"]

                    if isinstance(detail, list):
                        for error in detail:
                            st.error(error["msg"])
                    else:
                        st.error(detail)

            
                
    elif menu=='Login':
        st.header('LOGIN')
        with st.form('login_form'):
            username = st.text_input('username')
            password = st.text_input('password',type='password')
            login_clicked = st.form_submit_button('Login')
            if login_clicked:
                data = {
                    'username':username,
                    'password':password
                }
                response = login(data)
                
                if response.status_code==200:
                    logger.info(f"login successful :{username}")
                    st.success(f'Dear {username} -- login successful.')
                    
                    token = response.json()['access_token']
                    st.session_state['token']= token
                    st.query_params['token'] = token 
    
                    st.rerun()
                else:
                    logger.warning(f"login failed : {username}")
                    st.error(response.json().get('detail','login failed'))
else:
    st.header('Dashboard📋')
    st.write('WELCOME🙏🏻')
    headers= {"Authorization": f"Bearer {st.session_state['token']}"}
    
    response=get_current_user(headers)
    if response.status_code==200:
        user=response.json()
        st.write(f"welcome, {user['username']}👋🏻")
        st.write(f"Account Number : {user['account_number']}")

      

    option = st.sidebar.radio('Select Operation:',[
        'Deposit',
        'Withdraw',
        'Check Balance',
        'Transaction History',
        'Benefits'
        ])
    

        
        
    if option =='Deposit':
        st.subheader('deposit')
        with st.form('Deposit_form'):
            amount = st.number_input('Deposit Amount',min_value=0,step=100)
            deposit_clicked= st.form_submit_button('Deposit')
        if deposit_clicked:
            data= {
                'amount':amount }
            headers = {"Authorization":f"Bearer {st.session_state['token']}"
                                   }
            response =deposit(data, headers)
            
            if response.status_code==200:
                logger.info(f"amount deoposited successfully :{amount}")
                st.success('amount deposited successfully')
            else:
                logger.error(f"failed to deposit :{response.text}")
                st.error(response.json().get('detail','failed to deposit amount'))
                       
    elif option=='Withdraw':
        st.subheader('withdraw')
        with st.form('Withdraw_form'):
            amount = st.number_input('withdraw Amount',min_value=0,step=100)
            withdraw_clicked= st.form_submit_button('withdraw')
        if withdraw_clicked:
            data= {
                'amount':amount }
            headers = {"Authorization":f"Bearer {st.session_state['token']}"
                                   }
            response =withdraw(data, headers)
            
            if response.status_code==200:
                logger.info(f"withdrawal amount : {amount}")
                st.success('amount withdrawn successfully')
            else:
                logger.error(f"withdrawal failed :{response.text}")
                st.error(response.json().get('detail','failed to withdraw amount'))        
        

    elif option ==('Check Balance'):
        st.subheader('check balance')
        check = st.button('check-balance')
        if check:
            headers = {"Authorization":f"Bearer {st.session_state['token']}"
                       }
            response=balance(headers)
            data= response.json()
            
            st.write("account number : ", data["account_number"])
            st.write("holder name:", data["holder_name"])
            st.write("account type:", data["account_type"])
            st.write("Balance :",data["balance"])
            if response.status_code==200:
                logger.info(f"balance checked for account number")
                data = response.json()
                st.success(f"current balance :{data['balance']}")
            
            else:
                st.error(response.json().get('detail','failed to check balance'))
                        
    elif option =='Transaction History':
        st.subheader('transaction history')
        history=st.button('view history')
        if history:
            headers = {"Authorization":f"Bearer {st.session_state['token']}"}
            response=transaction(headers)
                        
            if response.status_code==200:
                
                transaction = response.json()
                if transaction:
                    logger.info(f"transaction history viewed")
                    st.dataframe(transaction)
                else:
                    st.info('no transaction found')
            
            else:
                st.error(response.json().get('detail','failed to get transaction history')) 
                           
    elif option=='Benefits':
        st.subheader('benefits')
        benefits_clicked=st.button('check benefits')
        if benefits_clicked:
            headers = {"Authorization":f"Bearer {st.session_state['token']}"
                       }
            response = benefits(headers)
            if response.status_code==200:
                logger.info(f"benefits viewed")
                st.write(response.json())
            else:
                st.error(response.json().get('detail','failed to check benefits'))
            
    
    if st.sidebar.button('Logout'):
        logger.info(f"user logged out")
        st.session_state.clear()
        st.query_params.clear()
        st.success('logged out successfully')
        st.rerun()