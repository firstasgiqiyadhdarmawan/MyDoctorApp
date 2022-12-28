import {StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {colors, fonts} from '../../../utils';

const IsMe = () => {
  return (
    <View style={styles.container}>
      <View style={styles.chatContent}>
        <Text style={styles.text}>
          Ibu dokter, apakah memakan jeruk tiap hari itu buruk?{' '}
        </Text>
      </View>
      <Text style={styles.date}>4.20 AM</Text>
    </View>
  );
};

export default IsMe;

const styles = StyleSheet.create({
  chatContent: {
    marginBottom: 20,
    padding: 12,
    borderRadius: 10,
    borderBottomRightRadius: 0,
    backgroundColor: colors.cardLight,
    maxWidth: '70%',
  },
  container: {
    marginBottom: 20,
    alignItems: 'flex-end',
    // paddingLeft: 16,
    paddingRight: 16,
    width: '100%',
  },
  text: {
    fontSize: 14,
    fontFamily: fonts.primary.normal,
    color: colors.text.primary,
  },
  date: {
    fontSize: 11,
    fontFamily: fonts.primary.normal,
    color: colors.text.secondary,
  },
});
