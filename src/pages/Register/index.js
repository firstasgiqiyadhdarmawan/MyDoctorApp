import {ScrollView, StyleSheet, View} from 'react-native';
import React, {useState} from 'react';
import {Button, Gap, Header, Input} from '../../components';
import {colors} from '../../utils';

const Register = ({navigation}) => {
  const [fullName, setFullName] = useState('');
  const [profession, setProfession] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <View style={styles.page}>
      <Header onPress={() => navigation.goBack()} title="Daftar Akun" />
      <View style={styles.content}>
        <ScrollView showsVerticalScrollIndicator={false}>
          <Input labelText={'Full Name'} />
          <Gap height={24} />
          <Input labelText={'Pekerjaan'} />
          <Gap height={24} />
          <Input labelText={'Email Address'} />
          <Gap height={24} />
          <Input labelText={'Password'} />
          <Gap height={40} />
          <Button
            title={'Continue'}
            onPress={() => navigation.replace('UploadPhoto')}
          />
        </ScrollView>
      </View>
    </View>
  );
};

export default Register;

const styles = StyleSheet.create({
  content: {
    padding: 40,
    paddingTop: 0,
  },
  page: {
    backgroundColor: colors.white,
    flex: 1,
  },
});
