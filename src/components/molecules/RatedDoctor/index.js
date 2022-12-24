import {Image, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {DummyDoctor1, IconStar} from '../../../assets';

const RatedDoctor = () => {
  return (
    <View>
      <Image source={DummyDoctor1} style={styles.avatar} />
      <Text>Alexa Rachel</Text>
      <Text>Pediatrician</Text>
      <IconStar />
      <IconStar />
      <IconStar />
      <IconStar />
      <IconStar />
    </View>
  );
};

export default RatedDoctor;

const styles = StyleSheet.create({
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 50 / 2,
  },
});
