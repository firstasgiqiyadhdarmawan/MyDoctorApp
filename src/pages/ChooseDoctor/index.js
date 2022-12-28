import React from 'react';
import {StyleSheet, View} from 'react-native';
import {
  DummyDoctor10,
  DummyDoctor11,
  DummyDoctor7,
  DummyDoctor8,
  DummyDoctor9,
} from '../../assets';
import {Header, ListDoctor} from '../../components';
import {colors} from '../../utils';

const ChooseDoctor = ({navigation}) => {
  return (
    <View style={styles.page}>
      <Header
        title="Pilih Dokter Anak"
        type="dark"
        onPress={() => navigation.goBack()}
      />
      <ListDoctor
        profile={DummyDoctor7}
        name="Alexander Jannie"
        desc="Wanita"
        type="next"
        onPress={() => navigation.navigate('Chatting')}
      />
      <ListDoctor
        profile={DummyDoctor8}
        name="John RenParker Steve"
        desc="Pria"
        type="next"
        onPress={() => navigation.navigate('Chatting')}
      />
      <ListDoctor
        profile={DummyDoctor9}
        name="Christable Hayza"
        desc="Wanita"
        type="next"
        onPress={() => navigation.navigate('Chatting')}
      />
      <ListDoctor
        profile={DummyDoctor10}
        name="James Aldvillia"
        desc="Pria"
        type="next"
        onPress={() => navigation.navigate('Chatting')}
      />
      <ListDoctor
        profile={DummyDoctor11}
        name="Natasha Tian Faith"
        desc="Wanita"
        type="next"
        onPress={() => navigation.navigate('Chatting')}
      />
    </View>
  );
};

export default ChooseDoctor;

const styles = StyleSheet.create({
  page: {
    backgroundColor: colors.white,
    flex: 1,
  },
});
