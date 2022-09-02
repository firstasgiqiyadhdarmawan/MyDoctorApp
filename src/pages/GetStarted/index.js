import {ImageBackground, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {ILLogo, ILGetStarted} from '../../assets';
import {Button, Gap} from '../../components';

const GetStarted = () => {
  return (
    <ImageBackground source={ILGetStarted} style={styles.page}>
      <View>
        <ILLogo />
        <Text style={styles.textTitle}>
          Konsultasi dengan dokter jadi lebih mudah & fleksibel
        </Text>
      </View>
      <View>
        <Button title={'Get Started'} />
        <Gap height={16} />
        <Button type={'secondary'} title={'Sign In'} />
      </View>
    </ImageBackground>
  );
};

export default GetStarted;

const styles = StyleSheet.create({
  page: {
    padding: 40,
    backgroundColor: 'white',
    justifyContent: 'space-between',
    flex: 1,
  },
  textTitle: {
    fontSize: 28,
    marginTop: 91,
    color: 'white',
    fontFamily: 'Nunito-SemiBold',
  },
});
