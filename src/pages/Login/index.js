import {ScrollView, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {ILLogo} from '../../assets';
import {Button, Gap, Input, Link} from '../../components';
import {colors, fonts} from '../../utils';
import axios from 'axios';

const Login = ({navigation}) => {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  const txthandler = txt => {
    setEmail(txt);
  };

  const SignIn = () => {
    // axios
    //   .get('https://dekontaminasi.com/api/id/covid19/hospitals')
    //   .then(response => {
    //     // setAdvice(response);
    //     console.log(response.data);
    //   });
    console.log(email);
    axios
      .post('https://tugasmd.as.r.appspot.com/login', {
        email: email,
        password: password,
      })
      .then(function (response) {
        console.log(response.data.user.email);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  return (
    <ScrollView style={styles.pagefull}>
      <View style={styles.page}>
        <ILLogo />
        <Text style={styles.title}>Masuk dan mulai berkonsultasi</Text>
        <Input
          labelText={'Email Address'}
          onChangeText={value => setEmail(value)}
          Value={email}
        />
        <Gap height={24} />
        <Input
          labelText={'Password'}
          onChangeText={value => setPassword(value)}
          Value={password}
          secureTextEntry={true}
        />
        <Gap height={10} />
        <Link title={'Forgot My Password'} size={12} />
        <Gap height={40} />
        <Button title="Sign In" onPress={() => SignIn()} />
        <Gap height={30} />
        <Link
          title={'Create New Account'}
          onPress={() => navigation.navigate('Register')}
          size={16}
          align={'center'}
        />
      </View>
    </ScrollView>
  );
};

export default Login;

const styles = StyleSheet.create({
  page: {
    padding: 40,
    backgroundColor: colors.white,
    flex: 1,
  },
  pagefull: {
    backgroundColor: colors.white,
    flex: 1,
  },
  title: {
    fontSize: 20,
    fontFamily: fonts.primary[600],
    color: colors.text.primary,
    marginTop: 40,
    marginBottom: 40,
    maxWidth: 153,
  },
});
