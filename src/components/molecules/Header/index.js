import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {colors, fonts} from '../../../utils';
import {Button, Gap} from '../../atoms';

const Header = ({onPress, title}) => {
  return (
    <View style={styles.container}>
      <Button type="icon-only" icon="IconBackDark" onPress={onPress} />
      <Text style={styles.text}>{title}</Text>
      <Gap width={24} />
    </View>
  );
};

export default Header;

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 16,
    backgroundColor: colors.white,
    paddingVertical: 30,
    flexDirection: 'row',
    alignItems: 'center',
  },
  text: {
    fontFamily: fonts.primary[600],
    fontSize: 20,
    fontWeight: '600',
    textAlign: 'center',
    flex: 1,
    color: colors.text.primary,
  },
});
