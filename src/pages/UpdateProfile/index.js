import {ScrollView, StyleSheet, Text, View} from 'react-native';
import React from 'react';
import {Button, Gap, Header, Input, Profile} from '../../components';
import {colors} from '../../utils';

const UpdateProfile = ({navigation}) => {
  return (
    <View style={styles.page}>
      <Header title="Edit Profile" onPress={() => navigation.goBack()} />
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.content}>
          <Profile isRemove />
          <Gap height={26} />
          <Input labelText="Full Name" />
          <Gap height={24} />
          <Input labelText="Pekerjaan" />
          <Gap height={24} />
          <Input labelText="Email" />
          <Gap height={24} />
          <Input labelText="Password" />
          <Gap height={40} />
          <Button
            title="Save Profile"
            onPress={() => navigation.goBack('UserProfile')}
          />
        </View>
      </ScrollView>
    </View>
  );
};

export default UpdateProfile;

const styles = StyleSheet.create({
  page: {flex: 1, backgroundColor: colors.white},
  content: {padding: 40, paddingTop: 0},
});
