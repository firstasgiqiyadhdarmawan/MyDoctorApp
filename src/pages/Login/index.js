import {StyleSheet, Text, View} from 'react-native';
import React from 'react';

const Login = () => {
  return (
    <View style={styles.page}>
      <Text>Login Page</Text>
    </View>
  );
};

export default Login;

const styles = StyleSheet.create({
  page: {
    padding: 40,
  },
});
