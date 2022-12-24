import {ScrollView, StyleSheet, View} from 'react-native';
import React from 'react';
import {Button, Gap, Header, Input} from '../../components';
import {colors} from '../../utils';

const Register = ({navigation}) => {
  return (
    <ScrollView>
      <View style={styles.page}>
        <Header onPress={() => navigation.goBack()} title="Daftar Akun" />
        <View style={styles.content}>
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
            onPress={() => navigation.navigate('UploadPhoto')}
          />
        </View>
      </View>
    </ScrollView>
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
