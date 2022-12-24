import {StyleSheet, Text, TextInput, View} from 'react-native';
import React from 'react';
import {colors, fonts} from '../../../utils';

const Input = ({labelText}) => {
  return (
    <View>
      <Text style={styles.labelText}>{labelText}</Text>
      <TextInput style={styles.input} />
    </View>
  );
};

export default Input;

const styles = StyleSheet.create({
  input: {
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: 10,
    padding: 12,
  },
  labelText: {
    fontSize: 16,
    fontFamily: fonts.primary[400],
    marginBottom: 6,
    color: colors.text.secondary,
  },
});
