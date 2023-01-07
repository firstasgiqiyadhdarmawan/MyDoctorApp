import {StyleSheet, Text, TextInput, View} from 'react-native';
import React, {useState} from 'react';
import {colors, fonts} from '../../../utils';

const Input = ({labelText}) => {
  const [border, setBorder] = useState(colors.border);
  const onFokusForm = () => {
    setBorder(colors.tertiary);
  };
  const onBlurForm = () => {
    setBorder(colors.border);
  };
  return (
    <View>
      <Text style={styles.labelText}>{labelText}</Text>
      <TextInput
        onFocus={onFokusForm}
        onBlur={onBlurForm}
        style={styles.input(border)}
      />
    </View>
  );
};

export default Input;

const styles = StyleSheet.create({
  input: border => ({
    borderWidth: 1,
    borderColor: border,
    borderRadius: 10,
    padding: 12,
  }),
  labelText: {
    fontSize: 16,
    fontFamily: fonts.primary[400],
    marginBottom: 6,
    color: colors.text.secondary,
  },
});
